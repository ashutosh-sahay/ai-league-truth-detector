"""Vector store management using ChromaDB."""

from __future__ import annotations

from functools import lru_cache

from langchain_chroma import Chroma
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
        collection_metadata={"hnsw:space": "cosine"}
    )


def add_documents(documents: list[Document]) -> None:
    """Add document chunks to the vector store and invalidate retriever caches."""
    if not documents:
        logger.warning("No documents to add.")
        return

    store = get_vector_store()
    store.add_documents(documents)
    logger.info(f"Added {len(documents)} document(s) to vector store.")

    # Invalidate cached retrievers so they rebuild with the new documents
    clear_retriever_caches()


def clear_retriever_caches() -> None:
    """Clear cached hybrid retriever and re-ranker so they rebuild with fresh data.

    Uses lazy imports to avoid circular dependency with retriever / re_ranker modules.
    """
    from src.rag.retriever import get_hybrid_retriever
    from src.rag.re_ranker import get_re_ranker_retriever

    get_hybrid_retriever.cache_clear()
    get_re_ranker_retriever.cache_clear()
    logger.info("Cleared retriever caches after document update.")


def get_all_documents() -> list[Document]:
    """Retrieve all documents stored in the vector store.

    Returns:
        List of Document objects with page_content and metadata.
    """
    store = get_vector_store()
    data = store.get(include=["documents", "metadatas"])
    documents = [
        Document(page_content=text, metadata=meta or {})
        for text, meta in zip(data["documents"], data["metadatas"])
    ]
    logger.info(f"Retrieved {len(documents)} document(s) from vector store.")
    return documents


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
