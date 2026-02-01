"""
Password Reset Token Model
==========================
SQLAlchemy model for password reset tokens.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta

from database import Base


class PasswordResetToken(Base):
    """Password Reset Token model"""
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PasswordResetToken for {self.email}>"

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
