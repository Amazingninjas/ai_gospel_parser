"""
Verse API Schemas
==================
Pydantic models for verse-related API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional


class VerseResponse(BaseModel):
    """Response model for verse lookup"""
    greek_text: str = Field(..., description="Original Greek text from SBLGNT")
    english_text: str = Field(..., description="English translation (WEB) for reference")
    book: str = Field(..., description="Book name (e.g., 'John')")
    chapter: int = Field(..., description="Chapter number")
    verse: int = Field(..., description="Verse number")
    reference: str = Field(..., description="Human-readable reference (e.g., 'John 3:16')")
    reference_id: str = Field(..., description="Internal ID (e.g., '64-03-16')")

    class Config:
        json_schema_extra = {
            "example": {
                "greek_text": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον...",
                "english_text": "For God so loved the world, that he gave his only born Son...",
                "book": "John",
                "chapter": 3,
                "verse": 16,
                "reference": "John 3:16",
                "reference_id": "64-03-16"
            }
        }


class VerseRangeResponse(BaseModel):
    """Response model for verse range lookup"""
    verses: list[VerseResponse]
    reference: str = Field(..., description="Human-readable range (e.g., 'John 3:16-18')")


class BookInfo(BaseModel):
    """Information about a Bible book"""
    name: str = Field(..., description="Full book name (e.g., 'John')")
    code: int = Field(..., description="Numeric book code (e.g., 64)")
    abbreviations: list[str] = Field(..., description="Common abbreviations (e.g., ['jn', 'joh'])")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "code": 64,
                "abbreviations": ["jn", "joh"]
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error (e.g., 'verse_not_found')")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Verse not found: John 3:100",
                "error_type": "verse_not_found"
            }
        }
