"""API route definitions."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

from src.agents.rag_agent import create_rag_agent

router = APIRouter()

# Compile the agent graph once at module level – the compiled graph is
# stateless and safe to reuse across requests.
_rag_agent = create_rag_agent()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class VerifyRequest(BaseModel):
    """Request body for the /verify endpoint."""

    claim: str = Field(..., min_length=1, description="The claim to verify.")


class VerifyResponse(BaseModel):
    """Response body for the /verify endpoint."""

    claim: str
    verification_data: str
    evidence_source: str  # "RAG Store" or "WEB"
    claim_verified: bool


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/health")
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok"}


@router.post("/verify", response_model=VerifyResponse)
async def verify_claim(request: VerifyRequest):
    """Verify a claim using the Agentic RAG pipeline.

    Workflow:
    1. Retrieve evidence from the RAG vector store
    2. Evaluate the claim against retrieved evidence
    3. If evidence is sufficient (confidence > 0.7) → return result
    4. Otherwise → web search → evaluate → sync to RAG store → return result
    """
    logger.info(f"Received claim: {request.claim[:100]}...")

    try:
        result = _rag_agent.invoke({"query": request.claim})

        # Extract the structured output from the last AI message
        ai_messages = [m for m in result["messages"] if hasattr(m, "content")]

        if ai_messages:
            try:
                output = json.loads(ai_messages[-1].content)
            except json.JSONDecodeError:
                # Fallback: build from state fields
                output = {
                    "claim": result.get("claim", request.claim),
                    "verification_data": result.get("verification_data", ai_messages[-1].content),
                    "evidence_source": result.get("evidence_source", "unknown"),
                    "claim_verified": result.get("claim_verified", False),
                }
        else:
            output = {
                "claim": request.claim,
                "verification_data": "No analysis produced.",
                "evidence_source": "unknown",
                "claim_verified": False,
            }

        return VerifyResponse(
            claim=output["claim"],
            verification_data=output["verification_data"],
            evidence_source=output["evidence_source"],
            claim_verified=output["claim_verified"],
        )
    except Exception as e:
        logger.error(f"Error verifying claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest")
async def ingest_documents():
    """Trigger document ingestion from the data/ directory."""
    from src.rag.ingestion import ingest
    from src.rag.vector_store import add_documents

    try:
        chunks = ingest()
        if not chunks:
            return {"status": "no documents found", "chunks": 0}
        add_documents(chunks)
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
