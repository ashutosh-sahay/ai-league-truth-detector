"""Tests for configuration module."""

from src.config import Settings


def test_default_settings():
    """Verify default settings load without errors."""
    s = Settings(openai_api_key="test-key")
    assert s.openai_model == "gpt-4o"
    assert s.chunk_size == 1000
    assert s.retriever_top_k == 5
    assert s.api_port == 8000
