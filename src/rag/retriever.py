"""High-level retrieval interface for the RAG pipeline."""

from __future__ import annotations

from functools import lru_cache

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from loguru import logger

from src.config import settings
from src.rag.vector_store import get_all_documents, get_vector_store


@lru_cache(maxsize=1)
def get_hybrid_retriever() -> EnsembleRetriever:
    """Return a hybrid retriever combining vector similarity and BM25 keyword search.

    Both retrievers operate over the same document set stored in the vector store.
    The result is cached; call ``clear_retriever_caches()`` after ingesting new
    documents.
    """
    vector_store = get_vector_store()
    vector_retriever = vector_store.as_retriever(
        search_kwargs={"k": settings.retriever_top_k},
    )

    # Load all documents from the vector store so BM25 indexes the same corpus
    documents = get_all_documents()

    if not documents:
        logger.warning(
            "Vector store is empty – BM25 retriever will be initialised with a "
            "placeholder document.  Ingest data to get meaningful results."
        )
        # BM25Retriever.from_documents requires at least one document
        documents = [Document(page_content="(empty knowledge base)", metadata={"source": "placeholder"})]

    bm25_retriever = BM25Retriever.from_documents(
        documents=documents, k=settings.retriever_top_k,
    )

    return EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever], weights=[0.7, 0.3],
    )


def get_context_after_re_ranker(query: str) -> list[Document]:
    """Retrieve documents via the hybrid retriever and re-rank them.

    Args:
        query: The search query string.

    Returns:
        Re-ranked list of documents relevant to the query.
    """
    # Lazy import to avoid circular dependency (re_ranker → retriever → re_ranker)
    from src.rag.re_ranker import get_re_ranker_retriever

    re_ranker_retriever = get_re_ranker_retriever()
    docs: list[Document] = re_ranker_retriever.invoke(query)
    logger.info(f"Re-ranker returned {len(docs)} document(s) for query: {query[:100]}")
    return docs