"""API route definitions."""

from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from loguru import logger

from src.agents.rag_agent import create_rag_agent

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class VerifyRequest(BaseModel):
    """Request body for the /verify endpoint."""

    claim: str = Field(..., min_length=1, description="The claim to verify.")


class VerifyResponse(BaseModel):
    """Response body for the /verify endpoint."""

    claim: str
    analysis: str
    # confidence: float = 0.0


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/health")
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok"}


@router.post("/verify", response_model=VerifyResponse)
async def verify_claim(request: VerifyRequest):
    """Verify a claim using the Agentic RAG pipeline."""
    logger.info(f"Received claim: {request.claim[:100]}...")

    try:
        agent = create_rag_agent()
        result = agent.invoke({"query": request.claim})

        # Extract the last AI message as the analysis
        ai_messages = [m for m in result["messages"] if hasattr(m, "content")]
        analysis = ai_messages[-1].content if ai_messages else "No analysis produced."

        return VerifyResponse(
            claim=request.claim,
            analysis=analysis,
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
