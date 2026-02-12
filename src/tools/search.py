"""Web search tool – placeholder for external search integration.

Replace the stub implementation with a real search provider
(e.g. Tavily, SerpAPI, Brave Search) when ready.
"""

from __future__ import annotations

from langchain_core.tools import tool


@tool
def web_search_tool(query: str) -> str:
    """Search the web for up-to-date information about a topic.

    Use this tool when the local knowledge base does not contain
    sufficient information to verify a claim.
    """
    # TODO: Integrate a real search provider (Tavily, SerpAPI, etc.)
    return (
        f"[Web search stub] No real search provider configured yet. "
        f"Query was: '{query}'. "
        "Please integrate a search API to enable this tool."
    )
