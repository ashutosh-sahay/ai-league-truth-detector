# AI League Truth Detector

An **Agentic RAG** (Retrieval-Augmented Generation) system for verifying claims and detecting misinformation, built with LangChain, LangGraph, ChromaDB, and FastAPI.

---

## Project Structure

```
├── src/
│   ├── agents/          # LangGraph agent definitions
│   │   ├── state.py     # Shared agent state
│   │   └── rag_agent.py # Core RAG agent graph
│   ├── rag/             # RAG pipeline
│   │   ├── ingestion.py # Document loading & chunking
│   │   ├── embeddings.py# Embedding model setup
│   │   ├── vector_store.py # ChromaDB operations
│   │   └── retriever.py # High-level retrieval interface
│   ├── tools/           # Agent tools
│   │   ├── retrieval.py # Vector store search tool
│   │   └── search.py    # Web search tool (stub)
│   ├── api/             # FastAPI application
│   │   ├── app.py       # App factory & middleware
│   │   └── routes.py    # API endpoints
│   ├── config.py        # Centralised settings
│   ├── logger.py        # Logging configuration
│   └── main.py          # Entry point
├── scripts/
│   └── ingest.py        # CLI script for document ingestion
├── tests/               # Test suite
├── data/                # Place documents here for ingestion
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Quick Start

### 1. Clone & enter the repo

```bash
git clone <repo-url>
cd ai-league-truth-detector
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 5. Ingest documents (optional)

Place `.txt` or `.pdf` files in the `data/` directory, then run:

```bash
python -m scripts.ingest
```

### 6. Start the API server

```bash
python -m src.main
```

The server starts at **http://localhost:8000**. API docs are available at **http://localhost:8000/docs**.

---

## API Endpoints

| Method | Endpoint            | Description                      |
|--------|---------------------|----------------------------------|
| GET    | `/api/v1/health`    | Health check                     |
| POST   | `/api/v1/verify`    | Verify a claim via Agentic RAG   |
| POST   | `/api/v1/ingest`    | Trigger document ingestion       |

### Example: Verify a claim

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The Earth revolves around the Sun"}'
```

---

## Running Tests

```bash
pytest
```

---

## Tech Stack

- **LangChain + LangGraph** – Agent orchestration & RAG chains
- **OpenAI** – LLM and embeddings
- **ChromaDB** – Vector storage & similarity search
- **FastAPI** – REST API layer
- **Pydantic** – Settings & data validation
- **Loguru** – Structured logging

---

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run `pytest` and `ruff check .` before pushing
4. Open a pull request
