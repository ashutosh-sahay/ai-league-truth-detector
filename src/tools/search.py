"""Web search tool using Tavily API for external search integration."""

from __future__ import annotations

from langchain_core.tools import tool
from loguru import logger
from tavily import TavilyClient

from src.config import settings


@tool
def web_search_tool(query: str) -> str:
    """Search the web for up-to-date information about a topic.

    Use this tool when the local knowledge base does not contain
    sufficient information to verify a claim.

    Args:
        query: The search query string

    Returns:
        Formatted search results with titles, URLs, and content snippets
    """
    try:
        if not settings.tavily_api_key:
            logger.error("Tavily API key not configured")
            return "Error: Tavily API key not configured. Please set TAVILY_API_KEY in .env"

        client = TavilyClient(api_key=settings.tavily_api_key)
        
        # Perform search with basic depth and limit results to 5
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=False,
            include_raw_content=False
        )
        
        if not response.get("results"):
            logger.warning(f"No web search results found for query: {query[:100]}")
            return "No relevant web search results found."
        
        # Format results for the LLM
        formatted_results = []
        for i, result in enumerate(response["results"], 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "No content available")
            
            formatted_results.append(
                f"[{i}] {title}\n"
                f"URL: {url}\n"
                f"Content: {content}"
            )
        
        logger.info(f"Retrieved {len(formatted_results)} web search results for query: {query[:100]}")
        return "\n\n---\n\n".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error performing web search: {e}")
        return f"Error performing web search: {str(e)}"
