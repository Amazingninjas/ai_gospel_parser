"""
Authentication Service
======================
Password hashing, JWT token generation, and user authentication.
"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from models.user import User
from models.password_reset_token import PasswordResetToken



# Password hashing
# Configure bcrypt to handle our pre-normalized passwords
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"  # Use bcrypt 2b variant for compatibility
)


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def _normalize_password(password: str) -> str:
        """
        Normalize password for bcrypt.

        Bcrypt has a 72-byte limit. For longer passwords, we pre-hash with SHA256.
        This is a standard security practice.
        """
        # Use >= 72 to be conservative (bcrypt limit is exactly 72 bytes)
        if len(password.encode('utf-8')) >= 72:
            # Pre-hash with SHA256 for long passwords
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
        return password

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        normalized_password = AuthService._normalize_password(plain_password)
        return pwd_context.verify(normalized_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        normalized_password = AuthService._normalize_password(password)
        return pwd_context.hash(normalized_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Data to encode in token (usually {"sub": user_email})
            expires_delta: Token expiration time (default: 7 days)

        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRATION_DAYS)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """
        Decode and validate a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            db: Database session
            email: User's email
            password: Plain text password

        Returns:
            User object if authenticated, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not AuthService.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def create_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            email: User's email
            password: Plain text password (will be hashed)
            full_name: User's full name (optional)

        Returns:
            Created User object
        """
        hashed_password = AuthService.get_password_hash(password)

        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_password_reset_token(db: Session, email: str) -> Optional[str]:
        """
        Create a password reset token for a user.

        Args:
            db: Database session
            email: User's email

        Returns:
            The reset token string or None if user not found.
        """
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None

        # Generate a secure, URL-safe token
        token = secrets.token_urlsafe(32)
        
        # Set expiration for 1 hour from now
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Store the token in the database
        token_record = PasswordResetToken(
            email=email,
            token=token,
            expires_at=expires_at
        )
        db.add(token_record)
        db.commit()

        return token

    @staticmethod
    def verify_reset_token(db: Session, token: str) -> Optional[str]:
        """
        Verify a password reset token.

        Args:
            db: Database session
            token: The reset token string

        Returns:
            The user's email if token is valid and not expired, otherwise None.
        """
        token_record = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()

        if not token_record:
            return None

        if token_record.is_expired():
            # Clean up expired token
            db.delete(token_record)
            db.commit()
            return None

        return token_record.email

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> Optional[User]:
        """
        Reset a user's password using a valid token.

        Args:
            db: Database session
            token: The reset token string
            new_password: The new plain text password

        Returns:
            The updated User object or None if token is invalid.
        """
        email = AuthService.verify_reset_token(db, token)
        if not email:
            return None

        user = AuthService.get_user_by_email(db, email)
        if not user:
            # Should not happen if token is valid, but good to check
            return None

        # Update password
        user.hashed_password = AuthService.get_password_hash(new_password)
        
        # Invalidate the token by deleting it
        token_record = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
        if token_record:
            db.delete(token_record)
        
        db.commit()

        return user
