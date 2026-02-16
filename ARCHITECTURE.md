# Architecture Diagrams for Presentation

## 1. High-Level System Architecture

```mermaid
flowchart TB
    subgraph UserLayer [User Interface]
        User[👤 User Input<br/>Chrome Extension or API Client<br/>Submits claims for verification]
    end
    
    subgraph APILayer [API Layer]
        API[🚀 FastAPI REST Server<br/>Port 8000<br/>Validates requests & routes to agent]
    end
    
    subgraph AgentLayer [Intelligent Agent Core]
        Agent[🤖 LangGraph Agent<br/>6-Node State Machine<br/>Decision Logic:<br/>• Try local RAG first<br/>• If confidence < 0.7 OR no results → Web search<br/>• Store web results back to RAG]
    end
    
    subgraph DataSources [Knowledge & Search Sources]
        RAG[(📚 ChromaDB Vector Store<br/>• Hybrid: Vector + BM25<br/>• FlashRank re-ranking<br/>• Self-improving storage)]
        LLM[🧠 OpenAI GPT-4o<br/>• Evidence evaluation<br/>• Confidence scoring: 0.0-1.0<br/>• Structured output]
        Web[🌐 Tavily Search API<br/>• Real-time web search<br/>• Returns 5 sources<br/>• With URLs for citation]
    end
    
    User -->|POST /verify| API
    API --> Agent
    
    Agent <-->|Query & Retrieve| RAG
    Agent <-->|Evaluate & Score| LLM
    Agent <-->|Search when needed| Web
    
    API -->|verdict + confidence + source URLs| User
    
    style UserLayer fill:#e3f2fd
    style APILayer fill:#fff3e0
    style AgentLayer fill:#f3e5f5
    style DataSources fill:#e8f5e9
    style User fill:#e3f2fd
    style API fill:#fff3e0
    style Agent fill:#f3e5f5
    style RAG fill:#e8f5e9
    style LLM fill:#fce4ec
    style Web fill:#e0f2f1
```

## 2. Request Flow Diagram

```mermaid
flowchart LR
    Start([User Claim])
    Retrieve[Retrieve<br/>Hybrid Search]
    EvalRAG[Evaluate<br/>RAG Evidence]
    Route{Confidence<br/>> 0.7?}
    WebSearch[Web<br/>Search]
    EvalWeb[Evaluate<br/>Web Evidence]
    Sync[Sync to<br/>RAG Store]
    Output([Return<br/>Verdict])
    
    Start --> Retrieve
    Retrieve --> EvalRAG
    EvalRAG --> Route
    Route -->|Yes| Output
    Route -->|No| WebSearch
    WebSearch --> EvalWeb
    EvalWeb --> Sync
    Sync --> Output
    
    style Start fill:#e3f2fd
    style Output fill:#e8f5e9
    style Route fill:#fff3e0
```

## 3. Hybrid Retrieval Pipeline

```mermaid
flowchart TB
    Query[User Query]
    
    subgraph Retrieval [Hybrid Retrieval]
        Vector[Vector Search<br/>Top 20<br/>Semantic]
        BM25[BM25 Search<br/>Top 20<br/>Keywords]
        Fusion[Ensemble Fusion<br/>70% Vector + 30% BM25]
    end
    
    Rerank[FlashRank Re-ranking<br/>Cross-Encoder]
    Top5[Top 5 Documents]
    
    Query --> Vector
    Query --> BM25
    Vector --> Fusion
    BM25 --> Fusion
    Fusion --> Rerank
    Rerank --> Top5
    
    style Query fill:#e3f2fd
    style Fusion fill:#fff3e0
    style Rerank fill:#fce4ec
    style Top5 fill:#e8f5e9
```

## 4. Self-Improving Knowledge Base

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant RAG as ChromaDB
    participant Web as Tavily
    
    Note over User,Web: First Query (Topic X)
    User->>Agent: Verify Claim
    Agent->>RAG: Search Local KB
    RAG-->>Agent: No Results
    Agent->>Web: Search Web
    Web-->>Agent: 5 Results + URLs
    Agent->>RAG: Store with Metadata
    Agent-->>User: Verdict + Source URLs
    
    Note over User,Web: Second Query (Same Topic)
    User->>Agent: Similar Claim
    Agent->>RAG: Search Local KB
    RAG-->>Agent: ✅ Found Cached Data
    Agent-->>User: Fast Response<br/>(No Web Search)
```

## 5. Data Storage with Source Attribution

```mermaid
flowchart LR
    Web[Web Search Results]
    
    subgraph Processing [Individual Processing]
        R1[Result 1<br/>URL + Title + Content]
        R2[Result 2<br/>URL + Title + Content]
        R3[Result 3<br/>URL + Title + Content]
    end
    
    subgraph Storage [ChromaDB Storage]
        C1[Chunk 1<br/>+ Metadata<br/>source_url, title]
        C2[Chunk 2<br/>+ Metadata<br/>source_url, title]
        C3[Chunk 3<br/>+ Metadata<br/>source_url, title]
    end
    
    Web --> R1
    Web --> R2
    Web --> R3
    
    R1 --> C1
    R2 --> C2
    R3 --> C3
    
    style Web fill:#e0f2f1
    style C1 fill:#e8f5e9
    style C2 fill:#e8f5e9
    style C3 fill:#e8f5e9
```

## 6. Complete Agent Graph (Detailed)

```mermaid
flowchart TB
    Start([🎯 START<br/>User Claim])
    
    Retrieve[📥 Node 1: Retrieve<br/>━━━━━━━━━━━━━━<br/>Vector Search Top 20<br/>BM25 Keyword Top 20<br/>Fusion + Re-rank → Top 5]
    
    EvalRAG[🧠 Node 2: Evaluate RAG<br/>━━━━━━━━━━━━━━<br/>GPT-4o analyzes evidence<br/>Returns: confidence score<br/>+ verdict + reasoning]
    
    Route{🔀 Node 3: Route<br/>━━━━━━━━━━━━━━<br/>evidence_found?<br/>AND<br/>confidence > 0.7?}
    
    WebSearch[🌐 Node 4: Web Search<br/>━━━━━━━━━━━━━━<br/>Tavily API<br/>5 results with URLs]
    
    EvalWeb[🧠 Node 5: Evaluate Web<br/>━━━━━━━━━━━━━━<br/>GPT-4o analyzes web data<br/>Extract source URLs]
    
    Sync[💾 Node 6: Sync to RAG<br/>━━━━━━━━━━━━━━<br/>Store each result with:<br/>source_url + title<br/>+ metadata in ChromaDB]
    
    Format[📦 Format Output<br/>━━━━━━━━━━━━━━<br/>verdict + confidence<br/>+ source URLs<br/>+ evidence source]
    
    End([✅ END<br/>Return Response])
    
    Start --> Retrieve
    Retrieve --> EvalRAG
    EvalRAG --> Route
    
    Route -->|✅ YES<br/>High Confidence| Format
    Route -->|❌ NO<br/>Need more data| WebSearch
    
    WebSearch --> EvalWeb
    EvalWeb --> Sync
    Sync --> Format
    
    Format --> End
    
    style Start fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    style End fill:#e8f5e9,stroke:#388e3c,stroke-width:3px
    style Route fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style EvalRAG fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style EvalWeb fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style Retrieve fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px
    style WebSearch fill:#e0f2f1,stroke:#00796b,stroke-width:2px
    style Sync fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Format fill:#fff9c4,stroke:#f9a825,stroke-width:2px
```
    style EvalWeb fill:#fce4ec
```

## 7. Tech Stack Overview

```mermaid
flowchart TB
    subgraph Frontend [Frontend Layer]
        Chrome[Chrome Extension<br/>JavaScript]
        API[FastAPI + Uvicorn<br/>Python REST API]
    end
    
    subgraph Agent [Agent Layer]
        LangGraph[LangGraph<br/>State Machine]
        LangChain[LangChain<br/>Tool Integration]
    end
    
    subgraph AI [AI Services]
        GPT[OpenAI GPT-4o<br/>LLM Evaluation]
        Embed[OpenAI Embeddings<br/>text-embedding-3-small]
        Tavily[Tavily Search<br/>Web Results]
    end
    
    subgraph Storage [Storage Layer]
        Chroma[ChromaDB<br/>Vector Database]
        BM25[BM25 Retriever<br/>Keyword Search]
        Flash[FlashRank<br/>Re-ranking]
    end
    
    Chrome --> API
    API --> LangGraph
    LangGraph --> LangChain
    LangChain --> GPT
    LangChain --> Embed
    LangChain --> Tavily
    LangChain --> Chroma
    LangChain --> BM25
    LangChain --> Flash
    
    style Frontend fill:#e3f2fd
    style Agent fill:#f3e5f5
    style AI fill:#fce4ec
    style Storage fill:#e8f5e9
```

## 8. API Response Structure

```mermaid
flowchart LR
    Input[Input:<br/>claim string]
    
    subgraph Response [API Response JSON]
        Claim[claim:<br/>Original claim]
        Verdict[claim_verdict:<br/>true / false]
        Data[verification_data:<br/>Detailed analysis]
        Source[evidence_source:<br/>RAG Store or WEB]
        URLs[source_urls:<br/>Array of URLs]
    end
    
    Input --> Response
    
    style Input fill:#e3f2fd
    style Verdict fill:#e8f5e9
    style URLs fill:#fff3e0
```

---

## Usage Instructions

1. Copy any diagram above
2. Paste into a Mermaid renderer:
   - https://mermaid.live/ (online editor)
   - VS Code with Mermaid extension
   - Notion, GitHub, or any Mermaid-compatible tool
3. Export as PNG/SVG
4. Insert into PowerPoint

## Recommended Diagrams for Presentation

- **Slide 1 (Overview)**: Diagram #1 - High-Level System Architecture
- **Slide 2 (Flow)**: Diagram #2 - Request Flow Diagram  
- **Slide 3 (Innovation)**: Diagram #3 - Hybrid Retrieval Pipeline
- **Slide 4 (Self-Improvement)**: Diagram #4 - Self-Improving Knowledge Base
- **Slide 5 (Technical)**: Diagram #6 - Complete Agent Graph
