"""
Chat API Schemas
================
Pydantic models for chat/AI-related requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ChatMessage(BaseModel):
    """Single chat message"""
    role: Literal["user", "assistant", "system"] = Field(
        ...,
        description="Message role (user, assistant, or system)"
    )
    content: str = Field(..., description="Message content")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What does agape mean in John 3:16?"
            }
        }


class ChatRequest(BaseModel):
    """Request to send a chat message"""
    message: str = Field(..., description="User's question or message")
    verse_reference: Optional[str] = Field(
        None,
        description="Current verse context (e.g., 'John 3:16')"
    )
    conversation_history: Optional[list[ChatMessage]] = Field(
        default_factory=list,
        description="Previous conversation messages for context"
    )
    include_lexicon: bool = Field(
        default=True,
        description="Include lexicon definitions in AI context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Explain the grammar of this verse",
                "verse_reference": "John 3:16",
                "conversation_history": [],
                "include_lexicon": True
            }
        }


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    response: str = Field(..., description="AI-generated response")
    verse_context: Optional[str] = Field(None, description="Verse context used")
    model: str = Field(..., description="AI model used (ollama/gemini)")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "The verb ἠγάπησεν is an aorist active indicative...",
                "verse_context": "John 3:16",
                "model": "ollama:mixtral"
            }
        }


class ChatStreamChunk(BaseModel):
    """Streamed chunk of AI response"""
    chunk: str = Field(..., description="Text chunk")
    done: bool = Field(default=False, description="Whether stream is complete")

    class Config:
        json_schema_extra = {
            "example": {
                "chunk": "The verb ",
                "done": False
            }
        }
