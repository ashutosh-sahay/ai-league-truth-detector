"""High-level retrieval interface for the RAG pipeline."""

from __future__ import annotations

from src.rag.vector_store import similarity_search


def retrieve_context(query: str, k: int | None = None) -> str:
    """Retrieve relevant context for a query and return as a formatted string.

    This is the main entry point used by the agent's retrieve node.
    """
    docs = similarity_search(query, k=k)
    if not docs:
        return "No relevant context found."

    # Format each chunk with its source metadata
    sections: list[str] = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        sections.append(f"[{i}] (source: {source})\n{doc.page_content}")

    return "\n\n---\n\n".join(sections)
