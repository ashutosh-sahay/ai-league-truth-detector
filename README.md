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
├── data/
│   └── Google.txt       # Sample knowledge base (Google article)
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

### 5. Ingest documents

The repo ships with `data/Google.txt` (a comprehensive article about Google). Ingest it into the vector store:

```bash
python -m scripts.ingest
```

You can also add more `.txt` or `.pdf` files to the `data/` directory and re-run the command.

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

### Example: Verify claims

The included `data/Google.txt` knowledge base lets you verify claims about Google. Here are some examples:

**True claim – founding date:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Google was founded on September 4, 1998, by Larry Page and Sergey Brin."}'
```

**True claim – initial investment:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Google received its first funding of $100,000 from Andy Bechtolsheim, co-founder of Sun Microsystems."}'
```

**False claim – CEO:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Jeff Bezos is the current CEO of Google."}'
```

**True claim – Alphabet restructuring:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "In 2015, Google was reorganized as a wholly owned subsidiary of Alphabet Inc."}'
```

**False claim – search engine name origin:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The name Google comes from the word galaxy."}'
```

**True claim – products:**

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Google develops the Android mobile operating system and the Chrome web browser."}'
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
