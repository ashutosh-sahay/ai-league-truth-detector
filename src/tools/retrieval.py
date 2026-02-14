"""Retrieval tool – lets the agent query the vector store on demand."""

from __future__ import annotations

from langchain_core.tools import tool

from src.rag.retriever import get_context_after_re_ranker


@tool
def retrieval_tool(query: str) -> str:
    """Search the knowledge base for information relevant to the query.

    Use this tool when you need to find evidence or supporting documents
    to verify a claim.
    """
    docs = get_context_after_re_ranker(query)
    if not docs:
        return "No relevant documents found in the knowledge base."

    sections: list[str] = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        sections.append(f"[{i}] (source: {source})\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)
