"""Tests — backend/llm_router.py (T-206)"""

import pytest
from unittest.mock import MagicMock, patch

from backend.llm_router import call_llm


def test_anthropic_provider():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="anthropic_result")]
    with patch("anthropic.Anthropic") as MockClient:
        MockClient.return_value.messages.create.return_value = mock_response
        result = call_llm("anthropic", "claude-3-haiku-20240307", "key", "prompt")
    assert result == "anthropic_result"


def test_openai_provider():
    mock_choice = MagicMock()
    mock_choice.message.content = "openai_result"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    with patch("openai.OpenAI") as MockClient:
        MockClient.return_value.chat.completions.create.return_value = mock_response
        result = call_llm("openai", "gpt-4o", "key", "prompt")
    assert result == "openai_result"


def test_google_provider():
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "google_result"
    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel", return_value=mock_model):
        result = call_llm("google", "gemini-2.0-flash", "key", "prompt")
    assert result == "google_result"


def test_ollama_provider():
    with patch("ollama.chat", return_value={"message": {"content": "ollama_result"}}):
        result = call_llm("ollama", "llama3", "", "prompt")
    assert result == "ollama_result"


def test_unknown_provider_raises():
    with pytest.raises(ValueError, match="Unsupported provider"):
        call_llm("unknown", "model", "key", "prompt")
