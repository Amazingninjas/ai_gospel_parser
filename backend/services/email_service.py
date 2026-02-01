"""
Email Service
=============
Handles sending password reset emails via SMTP.
Falls back to console logging if SMTP is not configured.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from config import settings

logger = logging.getLogger(__name__)


def send_password_reset_email(email: str, token: str):
    """
    Send a password reset email to the user.

    If SMTP is not configured, logs the reset link to console instead.

    Args:
        email: User's email address
        token: Password reset token
    """
    # Build reset link
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    # If SMTP not configured, log to console for development
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.info("=" * 70)
        logger.info("PASSWORD RESET LINK (SMTP not configured - development mode)")
        logger.info("=" * 70)
        logger.info(f"Email: {email}")
        logger.info(f"Reset Link: {reset_link}")
        logger.info("=" * 70)
        return

    # Build email message
    subject = "Password Reset Request"
    body = (
        f"Hello,\n\n"
        f"You requested a password reset. Click the link below to reset your password:\n\n"
        f"{reset_link}\n\n"
        f"This link will expire in 1 hour.\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"Thanks,\nThe AI Gospel Parser Team"
    )

    # Create message
    message = MIMEMultipart()
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
            logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {str(e)}")
        # Log the link as fallback
        logger.info(f"FALLBACK - Reset link for {email}: {reset_link}")
