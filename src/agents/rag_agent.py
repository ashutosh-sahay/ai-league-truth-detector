"""RAG Agent built with LangGraph.

This module defines the core agentic RAG workflow:
  1. Receive a user query (claim)
  2. Retrieve relevant context from the vector store
  3. Evaluate the claim against retrieved evidence (evidence_found, confidence)
  4. If evidence is strong (evidence_found=True & confidence > 0.7) → return result
  5. Otherwise fall back to web search → evaluate → sync new data into RAG store
  6. Return a structured verification result to the user
"""

from __future__ import annotations

import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from loguru import logger

from src.agents.state import AgentState, ClaimEvaluation
from src.config import settings
from src.rag.ingestion import ingest_text_content
from src.rag.retriever import get_context_after_re_ranker
from src.rag.vector_store import add_documents
from src.tools.search import web_search_tool

# ---------------------------------------------------------------------------
# Confidence threshold – claims with RAG confidence above this skip web search
# ---------------------------------------------------------------------------
CONFIDENCE_THRESHOLD = 0.7

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------
EVALUATE_CLAIM_PROMPT = """\
You are a Truth Detector assistant. Your job is to evaluate a claim against
the provided evidence and determine whether the claim is supported.

You MUST respond with a JSON object containing exactly these fields:
- "evidence_found" (bool): true if the evidence contains relevant information
  about the claim, false otherwise.
- "confidence" (float): your confidence score between 0.0 and 1.0 that the
  evidence adequately addresses the claim.
- "verification_data" (str): a detailed analysis explaining how the evidence
  supports or refutes the claim.
- "claim_verified" (bool): true if the claim is verified as true based on the
  evidence, false otherwise.

Guidelines:
- Always ground your answer in the provided evidence.
- If the evidence is insufficient or irrelevant, set evidence_found to false
  and confidence to a low value.
- Be concise but thorough in your verification_data.
"""


# ---------------------------------------------------------------------------
# Graph node functions
# ---------------------------------------------------------------------------


def retrieve_node(state: AgentState) -> dict:
    """Retrieve relevant documents from the vector store for the user's claim."""
    logger.info(f"Retrieving context for claim: {state.query[:100]}")
    documents = get_context_after_re_ranker(state.query)
    logger.info(f"Retrieved {len(documents)} document(s) from vector store")
    return {"context": documents, "claim": state.query}


def evaluate_rag_node(state: AgentState) -> dict:
    """Evaluate the claim against documents retrieved from the RAG store."""
    logger.info("Evaluating claim against RAG store evidence")

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    # Format retrieved documents as evidence text
    if state.context:
        evidence_parts = []
        for i, doc in enumerate(state.context, 1):
            source = doc.metadata.get("source", "unknown")
            evidence_parts.append(
                f"[{i}] (source: {source})\n{doc.page_content}"
            )
        evidence_text = "\n\n---\n\n".join(evidence_parts)
    else:
        evidence_text = "No documents were retrieved from the knowledge base."

    messages = [
        SystemMessage(content=EVALUATE_CLAIM_PROMPT),
        HumanMessage(
            content=(
                f"Claim to verify:\n{state.query}\n\n"
                f"Retrieved evidence from knowledge base:\n{evidence_text}\n\n"
                "Evaluate the claim and respond with the JSON object."
            )
        ),
    ]

    structured_llm = llm.with_structured_output(ClaimEvaluation)
    evaluation: ClaimEvaluation = structured_llm.invoke(messages)

    logger.info(
        f"RAG evaluation → evidence_found={evaluation.evidence_found}, "
        f"confidence={evaluation.confidence:.2f}, "
        f"claim_verified={evaluation.claim_verified}"
    )

    return {
        "evidence_found": evaluation.evidence_found,
        "confidence": evaluation.confidence,
        "verification_data": evaluation.verification_data,
        "claim_verified": evaluation.claim_verified,
        "evidence_source": "RAG Store",
    }


def route_after_evaluation(state: AgentState) -> str:
    """Route based on evidence quality from RAG evaluation.

    - If evidence_found=True AND confidence > CONFIDENCE_THRESHOLD (0.7) → format output directly
    - Otherwise → fall back to web search
    """
    if state.evidence_found and state.confidence > CONFIDENCE_THRESHOLD:
        logger.info(
            f"Sufficient RAG evidence (confidence={state.confidence:.2f}), "
            "routing to final output"
        )
        return "format_output"

    logger.info(
        f"Insufficient RAG evidence (evidence_found={state.evidence_found}, "
        f"confidence={state.confidence:.2f}), routing to web search"
    )
    return "web_search"


def web_search_node(state: AgentState) -> dict:
    """Perform web search when the RAG store lacks sufficient evidence."""
    logger.info(f"Performing web search for claim: {state.query[:100]}")
    web_results = web_search_tool.invoke({"query": state.query})
    return {"web_results": web_results}


def evaluate_web_node(state: AgentState) -> dict:
    """Evaluate the claim against web search results."""
    logger.info("Evaluating claim against web search results")

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    messages = [
        SystemMessage(content=EVALUATE_CLAIM_PROMPT),
        HumanMessage(
            content=(
                f"Claim to verify:\n{state.query}\n\n"
                f"Evidence from web search:\n{state.web_results}\n\n"
                "Evaluate the claim and respond with the JSON object."
            )
        ),
    ]

    structured_llm = llm.with_structured_output(ClaimEvaluation)
    evaluation: ClaimEvaluation = structured_llm.invoke(messages)

    logger.info(
        f"Web evaluation → evidence_found={evaluation.evidence_found}, "
        f"confidence={evaluation.confidence:.2f}, "
        f"claim_verified={evaluation.claim_verified}"
    )

    return {
        "evidence_found": evaluation.evidence_found,
        "confidence": evaluation.confidence,
        "verification_data": evaluation.verification_data,
        "claim_verified": evaluation.claim_verified,
        "evidence_source": "WEB",
    }


def sync_to_rag_node(state: AgentState) -> dict:
    """Sync web search results back into the RAG store for future queries.

    This ensures that knowledge discovered via web search is available
    for subsequent lookups without needing another web call.
    """
    logger.info("Syncing web search results to RAG store")

    if not state.web_results:
        logger.warning("No web results to sync")
        return {}

    try:
        # Ingest the raw web results as new documents
        chunks = ingest_text_content(
            content=state.web_results,
            metadata={"source": "web_search", "query": state.query},
        )
        if chunks:
            add_documents(chunks)
            logger.info(
                f"Synced {len(chunks)} chunk(s) from web results to RAG store"
            )
        else:
            logger.warning("No chunks produced from web results")
    except Exception as e:
        logger.error(f"Failed to sync web results to RAG store: {e}")

    return {}


def format_output_node(state: AgentState) -> dict:
    """Compile the final structured output and add it as an AI message."""
    output = {
        "claim": state.claim,
        "verification_data": state.verification_data,
        "evidence_source": state.evidence_source,
        "claim_verified": state.claim_verified,
    }

    logger.info(
        f"Final output → evidence_source={state.evidence_source}, "
        f"claim_verified={state.claim_verified}"
    )

    return {
        "messages": [
            AIMessage(content=json.dumps(output, indent=2))
        ],
    }


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def create_rag_agent() -> StateGraph:
    """Build and compile the agentic RAG graph.

    Workflow:
    1. retrieve        – Fetch documents from the vector store
    2. evaluate_rag    – LLM evaluates the claim against RAG evidence
    3. Route:
       a. confidence > 0.7 & evidence found → format_output → END
       b. otherwise → web_search → evaluate_web → sync_to_rag → format_output → END

    Returns a compiled LangGraph that can be invoked with:
        result = agent.invoke({"query": "Some claim to check"})
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("evaluate_rag", evaluate_rag_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("evaluate_web", evaluate_web_node)
    workflow.add_node("sync_to_rag", sync_to_rag_node)
    workflow.add_node("format_output", format_output_node)

    # Define edges
    workflow.set_entry_point("retrieve")

    # retrieve → evaluate_rag
    workflow.add_edge("retrieve", "evaluate_rag")

    # evaluate_rag → conditional routing
    workflow.add_conditional_edges(
        "evaluate_rag",
        route_after_evaluation,
        {"format_output": "format_output", "web_search": "web_search"},
    )

    # web_search → evaluate_web → sync_to_rag → format_output → END
    workflow.add_edge("web_search", "evaluate_web")
    workflow.add_edge("evaluate_web", "sync_to_rag")
    workflow.add_edge("sync_to_rag", "format_output")

    # format_output → END
    workflow.add_edge("format_output", END)

    return workflow.compile()
