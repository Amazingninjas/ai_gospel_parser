"""
Chat API Router
===============
WebSocket endpoint for streaming AI chat responses.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import Optional
import json

from schemas.chat import ChatMessage, ChatRequest, ChatResponse
from services.ai_service import AIService, get_ai_service
from services.verse_service import VerseService, get_verse_service
from services.lexicon_service import LexiconService, get_lexicon_service
from config import settings


router = APIRouter()


def extract_greek_words_from_verse(verse_text: str) -> list[str]:
    """
    Extract Greek words from verse text for lexicon lookup.

    Args:
        verse_text: Greek verse text

    Returns:
        List of Greek words (simplified extraction)
    """
    import re

    # Greek unicode range
    greek_pattern = r'[\u0370-\u03FF\u1F00-\u1FFF]+'
    greek_words = re.findall(greek_pattern, verse_text)

    # Remove duplicates and return first 5 unique words
    unique_words = []
    for word in greek_words:
        clean_word = word.strip('.,;:·')
        if clean_word and clean_word not in unique_words:
            unique_words.append(clean_word)

    return unique_words[:5]


def build_context(
    verse_reference: Optional[str],
    message: str,
    include_lexicon: bool,
    verse_service: VerseService,
    lexicon_service: LexiconService
) -> str:
    """
    Build context string for AI from verse and lexicon data.

    Args:
        verse_reference: Verse reference (e.g., "John 3:16")
        message: User's message (may contain Greek words)
        include_lexicon: Whether to include lexicon definitions
        verse_service: Verse lookup service
        lexicon_service: Lexicon lookup service

    Returns:
        Formatted context string
    """
    context_parts = []

    # Add verse context if provided
    if verse_reference:
        parsed = verse_service.parse_verse_reference(verse_reference)

        if parsed:
            # Handle single verse or range
            verses_to_include = [parsed] if isinstance(parsed, dict) else parsed

            for verse_ref in verses_to_include[:3]:  # Limit to 3 verses for context
                text, metadata = verse_service.lookup_verse(verse_ref)
                if text and metadata:
                    context_parts.append(f"""
{metadata['reference']}:
Greek: {text}
English (reference): {metadata.get('english_text', 'N/A')}
""")

    # Add lexicon context if requested
    if include_lexicon:
        # Extract Greek words from message and verse
        import re
        greek_pattern = r'[\u0370-\u03FF\u1F00-\u1FFF]+'
        greek_words = re.findall(greek_pattern, message)

        if greek_words:
            context_parts.append("\n=== LEXICON DEFINITIONS ===\n")

            for word in greek_words[:5]:  # Limit to 5 words
                word_clean = word.strip('.,;:·')
                entries = lexicon_service.lookup_by_greek(word_clean)

                for entry in entries[:1]:  # First match only
                    strongs = entry.get('strongs', '')
                    lemma = entry.get('lemma', '')
                    definition = entry.get('definition_strongs', '') or entry.get('definition_kjv', '')
                    pos = entry.get('part_of_speech', '')

                    context_parts.append(f"{strongs} {lemma} ({pos}): {definition}\n")

            context_parts.append("=== END LEXICON DEFINITIONS ===\n")

    return '\n'.join(context_parts)


@router.websocket("/stream")
async def chat_websocket(
    websocket: WebSocket,
    ai_service: AIService = Depends(get_ai_service),
    verse_service: VerseService = Depends(get_verse_service),
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    WebSocket endpoint for streaming AI chat.

    Client sends JSON messages:
    {
        "message": "What does agape mean?",
        "verse_reference": "John 3:16",  // optional
        "conversation_history": [...],    // optional
        "include_lexicon": true           // optional, default true
    }

    Server streams response chunks as JSON:
    {
        "chunk": "The word ",
        "done": false
    }

    Final message:
    {
        "chunk": "",
        "done": true
    }
    """
    await websocket.accept()
    print("✓ WebSocket connection established")

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                request_data = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "error": "Invalid JSON format",
                    "done": True
                })
                continue

            # Parse request
            message = request_data.get("message", "")
            verse_reference = request_data.get("verse_reference")
            conversation_history = request_data.get("conversation_history", [])
            include_lexicon = request_data.get("include_lexicon", True)

            if not message:
                await websocket.send_json({
                    "error": "Message is required",
                    "done": True
                })
                continue

            # Build context from verse and lexicon
            context = build_context(
                verse_reference,
                message,
                include_lexicon,
                verse_service,
                lexicon_service
            )

            # Stream AI response
            try:
                async for chunk in ai_service.chat_stream(
                    message,
                    conversation_history,
                    context
                ):
                    await websocket.send_json({
                        "chunk": chunk,
                        "done": False
                    })

                # Send completion signal
                await websocket.send_json({
                    "chunk": "",
                    "done": True
                })

            except Exception as e:
                print(f"⚠ Error during streaming: {e}")
                await websocket.send_json({
                    "error": f"AI service error: {str(e)}",
                    "done": True
                })

    except WebSocketDisconnect:
        print("✓ WebSocket connection closed")

    except Exception as e:
        print(f"⚠ WebSocket error: {e}")
        try:
            await websocket.send_json({
                "error": str(e),
                "done": True
            })
        except:
            pass


@router.get(
    "/info",
    summary="Get AI provider information",
    description="Get information about the configured AI provider (Ollama or Gemini)"
)
async def get_ai_info(
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Get AI provider information.

    Returns:
        Provider type, model, and status
    """
    return ai_service.get_provider_info()


@router.post(
    "/test",
    response_model=ChatResponse,
    summary="Test chat endpoint (non-streaming)",
    description="""
    Non-streaming chat endpoint for testing.

    For production use, prefer the WebSocket endpoint at /api/chat/stream
    which provides real-time streaming responses.
    """
)
async def test_chat(
    request: ChatRequest,
    ai_service: AIService = Depends(get_ai_service),
    verse_service: VerseService = Depends(get_verse_service),
    lexicon_service: LexiconService = Depends(get_lexicon_service)
):
    """
    Test chat endpoint (collects full response, no streaming).

    Args:
        request: Chat request with message and optional context

    Returns:
        Full AI response
    """
    # Build context
    context = build_context(
        request.verse_reference,
        request.message,
        request.include_lexicon,
        verse_service,
        lexicon_service
    )

    # Collect full response
    full_response = ""
    async for chunk in ai_service.chat_stream(
        request.message,
        [msg.dict() for msg in request.conversation_history],
        context
    ):
        full_response += chunk

    return ChatResponse(
        response=full_response,
        verse_context=request.verse_reference,
        model=f"{ai_service.provider_type}:{settings.OLLAMA_MODEL if ai_service.provider_type == 'ollama' else settings.GEMINI_MODEL}"
    )
