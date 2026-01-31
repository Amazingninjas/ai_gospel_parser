"""
Conversations API Router
========================
CRUD endpoints for managing conversation history.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.conversation import Conversation
from schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListItem
)
from routers.auth import get_current_user


router = APIRouter()


@router.get(
    "/",
    response_model=List[ConversationListItem],
    summary="List user's conversations",
    description="Get paginated list of user's conversation history"
)
async def list_conversations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's conversation history.

    Returns conversations sorted by most recently updated first.
    """
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(
        Conversation.updated_at.desc()
    ).offset(skip).limit(limit).all()

    # Format response
    result = []
    for conv in conversations:
        result.append(ConversationListItem(
            id=conv.id,
            title=conv.title or "Untitled Conversation",
            message_count=len(conv.messages) if conv.messages else 0,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        ))

    return result


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get conversation by ID",
    description="Retrieve full conversation details including all messages"
)
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get specific conversation with all messages.

    Only returns conversations owned by the current user.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        messages=conversation.messages or [],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.post(
    "/",
    response_model=ConversationResponse,
    status_code=201,
    summary="Create new conversation",
    description="Create a new conversation with optional initial messages"
)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conversation.

    If messages are provided, the title will be auto-generated from the first user message
    unless explicitly provided.
    """
    # Create conversation
    conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title,
        messages=[msg.dict() for msg in conversation_data.messages] if conversation_data.messages else []
    )

    # Auto-generate title if not provided and messages exist
    if not conversation.title and conversation_data.messages:
        for msg in conversation_data.messages:
            if msg.role == "user":
                conversation.title = msg.content[:50] + ("..." if len(msg.content) > 50 else "")
                break

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        messages=conversation.messages or [],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Update conversation",
    description="Update conversation title or append new messages"
)
async def update_conversation(
    conversation_id: int,
    conversation_data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a conversation.

    - If title is provided, updates the title
    - If messages are provided, REPLACES all existing messages

    To append messages, retrieve the conversation, add to the messages list, and send back.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Update title if provided
    if conversation_data.title is not None:
        conversation.title = conversation_data.title

    # Update messages if provided
    if conversation_data.messages is not None:
        conversation.messages = [msg.dict() for msg in conversation_data.messages]

    db.commit()
    db.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        messages=conversation.messages or [],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=ConversationResponse,
    summary="Append message to conversation",
    description="Add a single message to an existing conversation"
)
async def append_message(
    conversation_id: int,
    role: str = Query(..., description="Message role: 'user' or 'assistant'"),
    content: str = Query(..., description="Message content"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Append a single message to a conversation.

    This is more efficient than replacing all messages when you just want to add one.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Use the model's add_message method
    conversation.add_message(role, content)

    db.commit()
    db.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        messages=conversation.messages or [],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.delete(
    "/{conversation_id}",
    status_code=204,
    summary="Delete conversation",
    description="Permanently delete a conversation and all its messages"
)
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a conversation.

    This action cannot be undone.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()

    return None
