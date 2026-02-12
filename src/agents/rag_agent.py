"""RAG Agent built with LangGraph.

This module defines the core agentic RAG workflow:
  1. Receive a user query
  2. Retrieve relevant context from the vector store
  3. Reason over the context using an LLM
  4. Optionally use tools (search, retrieval) for multi-step reasoning
  5. Return a grounded answer with confidence score
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from src.agents.state import AgentState
from src.config import settings
from src.rag.retriever import retrieve_context

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
    context = retrieve_context(state.query)
    return {"context": context}


def reason_node(state: AgentState) -> dict:
    """Use the LLM to reason over retrieved context and produce an answer."""
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Claim to verify:\n{state.query}\n\n"
                f"Retrieved evidence:\n{state.context}\n\n"
                "Provide your analysis and a confidence score."
            )
        ),
    ]

    response = llm.invoke(messages)
    return {
        "messages": [AIMessage(content=response.content)],
    }


def should_continue(state: AgentState) -> str:
    """Decide whether to loop back for more retrieval or finish.

    Extend this function to add tool-use routing logic.
    """
    # For now, always end after one retrieve → reason pass.
    return "end"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def create_rag_agent() -> StateGraph:
    """Build and compile the agentic RAG graph.

    Returns a compiled LangGraph that can be invoked with:
        result = agent.invoke({"query": "Some claim to check"})
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("reason", reason_node)

    # Define edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "reason")
    workflow.add_conditional_edges(
        "reason",
        should_continue,
        {"end": END, "retrieve": "retrieve"},
    )

    return workflow.compile()
