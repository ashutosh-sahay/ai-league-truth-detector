"""RAG Agent built with LangGraph.

This module defines the core agentic RAG workflow:
  1. Receive a user query
  2. Retrieve relevant context from the vector store
  3. If context is not relevant, fall back to web search
  4. Reason over the context using an LLM
  5. Return a grounded answer with confidence score
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from loguru import logger

from src.agents.state import AgentState
from src.config import settings
from src.rag.retriever import retrieve_context
from src.tools.search import web_search_tool

# ---------------------------------------------------------------------------
# System prompt – customise for your truth-detection domain
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a Truth Detector assistant. Your job is to verify claims by analysing
retrieved evidence and reasoning step-by-step.

Guidelines:
- Always ground your answer in the provided context.
- If the context is insufficient, say so explicitly.
- Provide a confidence score between 0.0 and 1.0.
- Be concise but thorough.
"""


# ---------------------------------------------------------------------------
# Graph node functions
# ---------------------------------------------------------------------------


def retrieve_node(state: AgentState) -> dict:
    """Retrieve relevant documents for the user query."""
    context, is_relevant = retrieve_context(state.query)
    logger.info(f"Retrieved context, is_relevant={is_relevant}")
    return {"context": context, "is_relevant": is_relevant}


def web_search_node(state: AgentState) -> dict:
    """Perform web search when local knowledge base lacks relevant information."""
    logger.info(f"Performing web search for query: {state.query[:100]}")
    web_results = web_search_tool.invoke({"query": state.query})
    return {"web_results": web_results}


def reason_node(state: AgentState) -> dict:
    """Use the LLM to reason over retrieved context or web results and produce an answer."""
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    # Determine which evidence to use
    if state.web_results:
        # Use web search results
        evidence_source = "web search"
        evidence = state.web_results
        logger.info("Using web search results for reasoning")
    else:
        # Use local context
        evidence_source = "local knowledge base"
        evidence = state.context
        logger.info("Using local knowledge base for reasoning")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Claim to verify:\n{state.query}\n\n"
                f"Retrieved evidence (from {evidence_source}):\n{evidence}\n\n"
                "Provide your analysis and a confidence score."
            )
        ),
    ]

    response = llm.invoke(messages)
    return {
        "messages": [AIMessage(content=response.content)],
    }


def route_after_retrieve(state: AgentState) -> str:
    """Route to web search if context is not relevant, otherwise proceed to reasoning."""
    if not state.is_relevant:
        logger.info("Context not relevant, routing to web search")
        return "web_search"
    logger.info("Context is relevant, routing to reasoning")
    return "reason"


def should_continue(state: AgentState) -> str:
    """Decide whether to end after reasoning.

    After reasoning completes, always end the workflow.
    """
    return "end"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def create_rag_agent() -> StateGraph:
    """Build and compile the agentic RAG graph.

    Workflow:
    1. Retrieve from local vector store
    2. If not relevant -> web search -> reason -> end
    3. If relevant -> reason -> end

    Returns a compiled LangGraph that can be invoked with:
        result = agent.invoke({"query": "Some claim to check"})
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("reason", reason_node)

    # Define edges
    workflow.set_entry_point("retrieve")
    
    # After retrieve, route based on relevance
    workflow.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {"web_search": "web_search", "reason": "reason"},
    )
    
    # After web search, always proceed to reason
    workflow.add_edge("web_search", "reason")
    
    # After reason, check if we should end
    workflow.add_conditional_edges(
        "reason",
        should_continue,
        {"end": END},
    )

    return workflow.compile()
