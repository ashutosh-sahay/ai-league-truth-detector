"""API route definitions."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

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


def ingest_web_results_background(web_content: str, query: str) -> None:
    """Background task to ingest web search results into the vector store.

    Args:
        web_content: The web search results content
        query: The original query that triggered the web search
    """
    try:
        from src.rag.ingestion import ingest_text_content
        from src.rag.vector_store import add_documents

        logger.info(f"Starting background ingestion for query: {query[:100]}")

        # Create metadata for traceability
        metadata = {
            "source": "web_search",
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Ingest the web content
        chunks = ingest_text_content(content=web_content, metadata=metadata)

        if chunks:
            add_documents(chunks)
            logger.info(
                f"Successfully ingested {len(chunks)} chunk(s) from web search in background"
            )
        else:
            logger.warning("No chunks generated from web content")

    except Exception as e:
        logger.error(f"Error in background ingestion: {e}")


@router.get("/health")
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok"}


@router.post("/verify", response_model=VerifyResponse)
async def verify_claim(request: VerifyRequest, background_tasks: BackgroundTasks):
    """Verify a claim using the Agentic RAG pipeline.

    If the local knowledge base doesn't have relevant information,
    the agent will perform a web search. The web results will be
    returned to the user immediately, and then asynchronously
    ingested into the vector store for future queries.
    """
    logger.info(f"Received claim: {request.claim[:100]}...")

    try:
        agent = create_rag_agent()
        result = agent.invoke({"query": request.claim})

        # Extract the last AI message as the analysis
        ai_messages = [m for m in result["messages"] if hasattr(m, "content")]
        analysis = ai_messages[-1].content if ai_messages else "No analysis produced."

        # Check if web search was used (web_results field will be populated)
        if result.get("web_results"):
            logger.info("Web search was used, scheduling background ingestion")
            background_tasks.add_task(
                ingest_web_results_background,
                web_content=result["web_results"],
                query=request.claim,
            )

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
