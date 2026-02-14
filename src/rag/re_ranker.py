from __future__ import annotations

from functools import lru_cache

from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from loguru import logger

from src.config import settings
from src.rag.retriever import get_hybrid_retriever


@lru_cache(maxsize=1)
def get_re_ranker_retriever() -> ContextualCompressionRetriever:
    """Return a cached re-ranking retriever wrapping the hybrid retriever.

    Uses ``settings.retriever_top_n`` for the number of top results after
    re-ranking.  The result is cached; call ``clear_retriever_caches()``
    after ingesting new documents.
    """
    top_n = settings.retriever_top_n
    logger.info(f"Building re-ranker retriever with top_n={top_n}")
    compressor = FlashrankRerank(top_n=top_n)
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=get_hybrid_retriever(),
    )