"""Centralized configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings populated from .env file or environment."""

    # --- LLM ---
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # --- Vector Store ---
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "truth_detector"

    # --- RAG ---
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_top_k: int = 20
    retriever_top_n: int = 5
    similarity_threshold: float = 0.7

    # --- Web Search ---
    tavily_api_key: str = ""

    # --- API ---
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # --- Logging ---
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Singleton settings instance – import this wherever needed
settings = Settings()
