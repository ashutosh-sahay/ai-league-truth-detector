"""Vector store management using ChromaDB."""

from __future__ import annotations

from functools import lru_cache

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from loguru import logger

from src.config import settings
from src.rag.embeddings import get_embedding_model


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    """Return a persistent ChromaDB vector store instance."""
    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=get_embedding_model(),
        persist_directory=settings.chroma_persist_dir,
    )


def add_documents(documents: list[Document]) -> None:
    """Add document chunks to the vector store."""
    if not documents:
        logger.warning("No documents to add.")
        return

    store = get_vector_store()
    store.add_documents(documents)
    logger.info(f"Added {len(documents)} document(s) to vector store.")


def similarity_search(query: str, k: int | None = None) -> list[Document]:
    """Run a similarity search against the vector store."""
    k = k or settings.retriever_top_k
    store = get_vector_store()
    results = store.similarity_search(query, k=k)
    logger.debug(f"Retrieved {len(results)} result(s) for query: {query[:80]}...")
    return results


def similarity_search_with_scores(query: str, k: int | None = None) -> list[tuple[Document, float]]:
    """Run a similarity search and return documents with their similarity scores.

    Args:
        query: The search query string
        k: Number of results to return (defaults to retriever_top_k)

    Returns:
        List of tuples containing (Document, similarity_score)
        Lower scores indicate higher similarity in ChromaDB
    """
    k = k or settings.retriever_top_k
    store = get_vector_store()
    results = store.similarity_search_with_score(query, k=k)
    logger.debug(
        f"Retrieved {len(results)} result(s) with scores for query: {query[:80]}..."
    )
    return results
