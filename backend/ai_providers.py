"""
AI Provider abstraction layer for Gospel Parser.
Supports both Ollama (local) and Gemini (API) backends.
"""

import os
import sys
from typing import Iterator, List, Dict, Optional

# --- BASE PROVIDER CLASS ---

class AIProvider:
    """Base class for AI providers"""

    def chat(self, messages: List[Dict], stream: bool = True) -> Iterator[str]:
        """
        Send messages to AI and get response.

        Args:
            messages: List of {'role': 'user/assistant/system', 'content': 'text'}
            stream: If True, yield chunks as they arrive

        Yields:
            Response text chunks
        """
        raise NotImplementedError

    def test_connection(self) -> bool:
        """Test if provider is available"""
        raise NotImplementedError


# --- OLLAMA PROVIDER ---

class OllamaProvider(AIProvider):
    """Ollama local LLM provider"""

    def __init__(self, model: str = "mixtral", host: str = "http://localhost:11434"):
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError("ollama package not installed. Run: pip install ollama")

        self.model = model
        self.client = ollama.Client(host=host)
        self.host = host

    def chat(self, messages: List[Dict], stream: bool = True) -> Iterator[str]:
        """Stream chat response from Ollama"""
        response = self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream
        )

        if stream:
            for chunk in response:
                yield chunk['message']['content']
        else:
            yield response['message']['content']

    def test_connection(self) -> bool:
        """Test Ollama connection"""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def get_info(self) -> str:
        return f"Ollama ({self.model}) at {self.host}"


# --- GEMINI PROVIDER ---

class GeminiProvider(AIProvider):
    """Google Gemini API provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        try:
            import google.generativeai as genai
            self.genai = genai
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )

        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GOOGLE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        self.genai.configure(api_key=self.api_key)
        self.model_name = model
        self.model = self.genai.GenerativeModel(model)

    def chat(self, messages: List[Dict], stream: bool = True) -> Iterator[str]:
        """Stream chat response from Gemini"""
        # Convert messages format to Gemini format
        gemini_messages = self._convert_messages(messages)

        response = self.model.generate_content(
            gemini_messages,
            stream=stream
        )

        if stream:
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        else:
            yield response.text

    def _convert_messages(self, messages: List[Dict]) -> str:
        """Convert OpenAI-style messages to Gemini prompt format"""
        # Gemini uses a simpler prompt format
        # Combine system message and user messages into a single prompt

        prompt_parts = []

        for msg in messages:
            role = msg['role']
            content = msg['content']

            if role == 'system':
                prompt_parts.append(f"SYSTEM INSTRUCTIONS:\n{content}\n")
            elif role == 'user':
                prompt_parts.append(f"USER: {content}\n")
            elif role == 'assistant':
                prompt_parts.append(f"ASSISTANT: {content}\n")

        return "\n".join(prompt_parts)

    def test_connection(self) -> bool:
        """Test Gemini API connection"""
        try:
            # Try a simple generation
            response = self.model.generate_content("Test", stream=False)
            return bool(response.text)
        except Exception:
            return False

    def get_info(self) -> str:
        return f"Google Gemini ({self.model_name})"


# --- PROVIDER FACTORY ---

def get_provider(provider_type: str = "ollama", **kwargs) -> AIProvider:
    """
    Factory function to get AI provider.

    Args:
        provider_type: "ollama" or "gemini"
        **kwargs: Provider-specific arguments

    Returns:
        AIProvider instance
    """
    provider_type = provider_type.lower()

    if provider_type == "ollama":
        return OllamaProvider(**kwargs)
    elif provider_type == "gemini":
        return GeminiProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")


# --- AUTO-DETECT OLLAMA HOST (WSL SUPPORT) ---

def get_ollama_host() -> str:
    """Get the appropriate Ollama host (handles WSL to Windows connection)"""
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if 'nameserver' in line:
                    host_ip = line.split()[1]
                    return f"http://{host_ip}:11434"
    except:
        pass
    return "http://localhost:11434"
