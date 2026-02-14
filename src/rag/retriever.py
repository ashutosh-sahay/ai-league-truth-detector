"""High-level retrieval interface for the RAG pipeline."""

from __future__ import annotations

from loguru import logger

from src.config import settings
from src.rag.vector_store import similarity_search_with_scores


def retrieve_context(query: str, k: int | None = None) -> tuple[str, bool]:
    """Retrieve relevant context for a query and return as a formatted string with relevance indicator.

    This is the main entry point used by the agent's retrieve node.

    Args:
        query: The search query string
        k: Number of results to return (defaults to retriever_top_k)

    Returns:
        Tuple of (formatted_context, is_relevant)
        - formatted_context: String with retrieved documents
        - is_relevant: Boolean indicating if top result meets similarity threshold
    """
    docs_with_scores = similarity_search_with_scores(query, k=k)
    
    if not docs_with_scores:
        logger.info(f"No documents found for query: {query[:100]}")
        return "No relevant context found.", False
    
    # Check if the top result meets the similarity threshold
    # Note: ChromaDB returns L2 distance scores where lower is better (0 = perfect match)
    # The distance can range from 0 to infinity, but typically meaningful scores are < 2.0
    top_score = docs_with_scores[0][1]
    
    # Convert similarity_threshold (0.7 = 70% similar) to a distance threshold
    # Using a more lenient formula: distance_threshold = 2.5 * (1 - similarity_threshold)
    # similarity_threshold=0.7 -> distance_threshold=0.75
    # similarity_threshold=0.5 -> distance_threshold=1.25
    distance_threshold = 2.5 * (1 - settings.similarity_threshold)
    is_relevant = top_score <= distance_threshold
    
    logger.info(
        f"Top distance score: {top_score:.3f} (lower is better), "
        f"Distance threshold: {distance_threshold:.3f}, "
        f"Is relevant: {is_relevant}"
    )
    
    # Format each chunk with its source metadata and score
    sections: list[str] = []
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        source = doc.metadata.get("source", "unknown")
        sections.append(
            f"[{i}] (source: {source}, score: {score:.3f})\n{doc.page_content}"
        )
    
    formatted_context = "\n\n---\n\n".join(sections)
    return formatted_context, is_relevant
