"""Retrieval tool – lets the agent query the vector store on demand."""

from __future__ import annotations

from langchain_core.tools import tool

from src.rag.retriever import retrieve_context


@tool
def retrieval_tool(query: str) -> str:
    """Search the knowledge base for information relevant to the query.

    Use this tool when you need to find evidence or supporting documents
    to verify a claim.
    """
    return retrieve_context(query)
