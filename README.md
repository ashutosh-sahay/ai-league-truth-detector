# AI League Truth Detector

An **Agentic RAG** (Retrieval-Augmented Generation) system for verifying claims and detecting misinformation, built with LangChain, LangGraph, ChromaDB, Tavily, and FastAPI.

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
│   │   └── search.py    # Tavily web search integration
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
```

Edit `.env` and add your API keys:

```bash
# Required: OpenAI API key for LLM and embeddings
OPENAI_API_KEY=your-openai-api-key-here

# Required: Tavily API key for web search fallback
TAVILY_API_KEY=your-tavily-api-key-here

# Optional: Similarity threshold for determining relevance (default: 0.7)
SIMILARITY_THRESHOLD=0.7
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/ (sign up for free API access)

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

## How It Works

The system uses an intelligent multi-stage verification workflow:

1. **Local Retrieval**: Query is first searched against the local vector store (ChromaDB)
2. **Relevance Check**: Similarity scores are evaluated against a configurable threshold (default: 0.7)
3. **Intelligent Fallback**:
   - If local context is relevant → LLM analyzes using local knowledge
   - If local context is insufficient → Tavily web search is triggered
4. **Web Search Integration**: Fresh information is retrieved from the web via Tavily API
5. **Immediate Response**: LLM analyzes web results and returns verdict to user
6. **Background Ingestion**: Web results are asynchronously embedded and added to vector store for future queries

This creates a **self-improving knowledge base** that expands automatically based on user queries.

### Similarity Scoring and Threshold Logic

Understanding how the system determines relevance:

#### Distance Scores (ChromaDB)

ChromaDB uses **L2 distance** for similarity search, where:
- **Lower scores = higher similarity** (0 = perfect match)
- Typical meaningful scores range from `0.0` to `2.0`
- Scores > `2.0` indicate very low similarity

#### Threshold Calculation

The `SIMILARITY_THRESHOLD` setting (default: `0.7` = 70% similarity) is converted to a distance threshold:

```
distance_threshold = 2.5 × (1 - SIMILARITY_THRESHOLD)
```

**Examples:**
- `SIMILARITY_THRESHOLD=0.7` → `distance_threshold=0.75`
- `SIMILARITY_THRESHOLD=0.5` → `distance_threshold=1.25`
- `SIMILARITY_THRESHOLD=0.9` → `distance_threshold=0.25` (very strict)

#### Decision Logic

```
If top_result_distance <= distance_threshold:
    Use local knowledge base ✅
Else:
    Trigger web search 🔍
```

#### Tuning Recommendations

Adjust `SIMILARITY_THRESHOLD` based on your needs:

| Threshold | Distance | Behavior | Use Case |
|-----------|----------|----------|----------|
| `0.9` | `0.25` | Very strict - requires near-exact matches | High-precision, avoid false positives |
| `0.7` | `0.75` | Balanced (default) | General purpose |
| `0.5` | `1.25` | Lenient - accepts broader matches | Maximize local KB usage, reduce API costs |
| `0.3` | `1.75` | Very lenient | Minimize web searches |

**Monitoring in Logs:**

Watch for these log entries to track decision-making:
```
INFO | Top distance score: 0.639 (lower is better), Distance threshold: 0.75, Is relevant: True
INFO | Context is relevant, routing to reasoning
```

or

```
INFO | Top distance score: 0.870 (lower is better), Distance threshold: 0.75, Is relevant: False
INFO | Context not relevant, routing to web search
```

---

## API Endpoints

| Method | Endpoint            | Description                                    |
|--------|---------------------|------------------------------------------------|
| GET    | `/api/v1/health`    | Health check                                   |
| POST   | `/api/v1/verify`    | Verify a claim (with intelligent web fallback) |
| POST   | `/api/v1/ingest`    | Trigger document ingestion from data/ folder   |

### Example: Verify claims

#### Claims about Google (from local knowledge base)

The included `data/Google.txt` knowledge base lets you verify claims about Google. These will be answered from local context:

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

#### Claims requiring web search (not in local KB)

For claims outside the local knowledge base, the system automatically falls back to web search:

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The Eiffel Tower is located in Paris, France."}'
```

```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Python 3.12 was released in October 2023."}'
```

**Note**: After web search, the retrieved information is automatically added to the vector store. Subsequent queries about the same topic will use the cached local knowledge.

---

## Running Tests

```bash
pytest
```

---

## Tech Stack

- **LangChain + LangGraph** – Agent orchestration & RAG chains
- **OpenAI** – LLM (GPT-4o) and embeddings (text-embedding-3-small)
- **Tavily** – Web search API for real-time information retrieval
- **ChromaDB** – Vector storage & similarity search
- **FastAPI** – REST API layer with async background tasks
- **Pydantic** – Settings & data validation
- **Loguru** – Structured logging

---

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run `pytest` and `ruff check .` before pushing
4. Open a pull request
