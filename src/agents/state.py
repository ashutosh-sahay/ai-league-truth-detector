"""Agent state definitions for LangGraph."""

from __future__ import annotations

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.documents import Document


class ClaimEvaluation(BaseModel):
    """Structured output from the LLM when evaluating a claim against evidence."""

    evidence_found: bool = Field(
        description="Whether relevant evidence was found to evaluate the claim"
    )
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0 in the evaluation"
    )
    verification_data: str = Field(
        description="Detailed analysis and evidence supporting the evaluation"
    )
    claim_verified: bool = Field(
        description="Whether the claim is verified as true based on the evidence"
    )


class AgentState(BaseModel):
    """Shared state that flows through the agent graph.

    Extend this class to add domain-specific fields as the project evolves.
    """

    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)

    # --- Query ---
    query: str = ""  # The user's claim to verify

    # --- RAG retrieval ---
    context: list[Document] = []  # Documents retrieved from the vector store
    evidence_found: bool = False  # Whether evidence was found in the context
    confidence: float = 0.0  # Confidence score (0.0 – 1.0)

    # --- Web search fallback ---
    web_results: str = ""  # Raw web search results

    # --- Final output fields ---
    claim: str = ""  # Echo of the user query (claim)
    verification_data: str = ""  # Evidence / analysis text (from RAG or Web)
    evidence_source: str = ""  # "RAG Store" or "WEB"
    claim_verified: bool = False  # Whether the claim is verified as true