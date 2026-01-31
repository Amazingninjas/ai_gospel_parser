"""
Conversation Model
==================
SQLAlchemy model for chat conversation history.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Conversation(Base):
    """Conversation history model"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=True)  # Auto-generated from first message
    messages = Column(JSON, nullable=False, default=list)  # List of {role, content} dicts
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")

    def __repr__(self):
        return f"<Conversation {self.id} - {self.title or 'Untitled'}>"

    def add_message(self, role: str, content: str):
        """Add a message to the conversation"""
        if not self.messages:
            self.messages = []

        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()

        # Auto-generate title from first user message
        if not self.title and role == "user":
            # Use first 50 chars as title
            self.title = content[:50] + ("..." if len(content) > 50 else "")
