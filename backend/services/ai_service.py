"""
AI Chat Service
===============
Wraps ai_providers.py for API use with streaming support.
"""
import sys
from pathlib import Path
from typing import AsyncGenerator, Optional

# Add parent directory to path to import existing code
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import settings
from ai_providers import get_provider


class AIService:
    """
    Service for AI chat using existing Ollama/Gemini providers.

    Supports streaming responses for real-time user experience.
    """

    def __init__(self):
        """Initialize AI provider based on configuration"""
        self.provider = None
        self.provider_type = settings.AI_PROVIDER
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the configured AI provider"""
        try:
            if self.provider_type == "ollama":
                self.provider = get_provider(
                    "ollama",
                    model=settings.OLLAMA_MODEL,
                    host=settings.OLLAMA_HOST
                )
                print(f"✓ AI Provider initialized: Ollama ({settings.OLLAMA_MODEL})")

            elif self.provider_type == "gemini":
                self.provider = get_provider(
                    "gemini",
                    model=settings.GEMINI_MODEL
                )
                print(f"✓ AI Provider initialized: Gemini ({settings.GEMINI_MODEL})")

            else:
                raise ValueError(f"Unknown AI provider: {self.provider_type}")

        except Exception as e:
            print(f"⚠ Error initializing AI provider: {e}")
            if self.provider_type == "ollama":
                print(f"   Make sure Ollama is running at: {settings.OLLAMA_HOST}")
                print(f"   And model is downloaded: ollama pull {settings.OLLAMA_MODEL}")
            elif self.provider_type == "gemini":
                print(f"   Make sure GEMINI_API_KEY is set in .env")
            raise

    def get_system_message(self) -> str:
        """Get the system message for AI context"""
        return """You are an expert research assistant specializing in the Greek Bible.

CRITICAL INSTRUCTION: You must answer questions based EXCLUSIVELY on the GREEK TEXT provided in the context.

The English text is provided ONLY as a reference for verse identification and navigation.
DO NOT quote, analyze, reference, or mention the English text in your responses UNLESS
the user explicitly asks for it (e.g., "compare with English", "show me the English",
"what does the English say").

Your responses should focus on:
- Greek word meanings, etymology, and usage
- Greek grammar, syntax, and word order
- Strong's numbers and lexical definitions
- Original Greek text analysis and interpretation
- Manuscript variants (when relevant)

Always cite Greek text and references. Be scholarly and precise."""

    async def chat_stream(
        self,
        message: str,
        conversation_history: list[dict],
        context: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream AI response chunk by chunk.

        Args:
            message: User's message/question
            conversation_history: Previous conversation messages
            context: Optional context (verse text, lexicon data, etc.)

        Yields:
            Response chunks as they are generated
        """
        # Build messages for AI
        messages = [{'role': 'system', 'content': self.get_system_message()}]

        # Add conversation history (limit to last 10 exchanges)
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        messages.extend(recent_history)

        # Add current message with context
        if context:
            current_message = f"""CONTEXT FROM GREEK BIBLICAL TEXTS:
---
{context}
---

USER QUESTION: {message}

REMEMBER: Focus ONLY on the Greek text. Do not reference English unless explicitly asked.
When citing lexicon definitions, mention "According to Thayer's lexicon..." for attribution."""
        else:
            current_message = message

        messages.append({'role': 'user', 'content': current_message})

        # Stream response
        try:
            async for chunk in self._stream_from_provider(messages):
                yield chunk

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"⚠ {error_msg}")
            yield error_msg

    async def _stream_from_provider(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """
        Stream response from the AI provider in real-time.

        Args:
            messages: List of conversation messages

        Yields:
            Response chunks as they arrive
        """
        import asyncio

        try:
            # Run synchronous streaming in thread executor
            # This allows async iteration over sync generator
            loop = asyncio.get_event_loop()

            print("→ Starting AI streaming...")
            chunk_count = 0

            # Create iterator in executor
            def get_chunks():
                for chunk in self.provider.chat(messages, stream=True):
                    yield chunk

            # Stream chunks as they arrive
            chunks_iter = get_chunks()
            while True:
                try:
                    # Get next chunk in executor (non-blocking)
                    chunk = await loop.run_in_executor(None, next, chunks_iter, None)
                    if chunk is None:
                        break
                    chunk_count += 1
                    yield chunk
                except StopIteration:
                    break

            print(f"✓ Streaming complete ({chunk_count} chunks)")

        except Exception as e:
            print(f"⚠ Provider streaming error: {e}")
            raise RuntimeError(f"Provider streaming error: {e}")

    def get_provider_info(self) -> dict:
        """
        Get information about the current AI provider.

        Returns:
            Dict with provider type and model
        """
        return {
            "type": self.provider_type,
            "model": settings.OLLAMA_MODEL if self.provider_type == "ollama" else settings.GEMINI_MODEL,
            "info": self.provider.get_info() if self.provider else "Not initialized"
        }


# Singleton instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get singleton instance of AIService (dependency injection)"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
