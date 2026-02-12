"""Embedding utilities – create and manage embedding models."""

from __future__ import annotations

from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from src.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> OpenAIEmbeddings:
    """Return a cached embedding model instance.

    Uses OpenAI embeddings by default. Swap this out for
    sentence-transformers or another provider if preferred.
    """
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
