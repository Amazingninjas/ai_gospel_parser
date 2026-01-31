"""
Conversation Schemas
====================
Pydantic schemas for conversation API requests/responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ConversationMessage(BaseModel):
    """Single message in a conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp (ISO format)")


class ConversationCreate(BaseModel):
    """Request to create a new conversation"""
    title: Optional[str] = Field(None, description="Conversation title (auto-generated if not provided)")
    messages: Optional[List[ConversationMessage]] = Field(default_factory=list, description="Initial messages")


class ConversationUpdate(BaseModel):
    """Request to update a conversation"""
    title: Optional[str] = Field(None, description="New conversation title")
    messages: Optional[List[ConversationMessage]] = Field(None, description="Messages to add/replace")


class ConversationResponse(BaseModel):
    """Response with conversation data"""
    id: int
    user_id: int
    title: Optional[str]
    messages: List[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationListItem(BaseModel):
    """Conversation summary for list view"""
    id: int
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
