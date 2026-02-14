"""Document ingestion – load, split, and prepare documents for embedding."""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from src.config import settings


def load_documents(data_dir: str | Path = "data") -> list[Document]:
    """Load documents from the data directory.

    Supports .txt and .pdf files out of the box.
    Add more loaders here as needed (e.g. DOCX, HTML, CSV).
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        logger.warning(f"Data directory '{data_path}' does not exist.")
        return []

    documents: list[Document] = []

    # Load text files
    txt_loader = DirectoryLoader(
        str(data_path), glob="**/*.txt", loader_cls=TextLoader, show_progress=True
    )
    documents.extend(txt_loader.load())


    logger.info(f"Loaded {len(documents)} document(s) from '{data_path}'.")
    return documents

def load_text_content(content: str) -> list[Document]:
    document = Document(page_content=content, metadata={"source": "text"})
    return [document]

def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks suitable for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunk(s).")
    return chunks


def ingest(data_dir: str | Path = "data") -> list[Document]:
    """End-to-end ingestion pipeline: load → split → return chunks."""
    docs = load_documents(data_dir)
    if not docs:
        return []
    return split_documents(docs)


def ingest_text_content(content: str, metadata: dict | None = None) -> list[Document]:
    """Ingest raw text content directly without file operations.

    This function is useful for ingesting web search results or other
    dynamically retrieved content.

    Args:
        content: Raw text content to ingest
        metadata: Optional metadata dictionary to attach to the document

    Returns:
        List of document chunks ready for embedding
    """
    if not content:
        logger.warning("Empty content provided for ingestion")
        return []

    # Split the document into chunks using the existing splitter
    chunks = split_documents(load_text_content(content))

    # Apply caller-supplied metadata to every chunk so provenance is preserved
    if metadata:
        for chunk in chunks:
            chunk.metadata.update(metadata)

    logger.info(f"Ingested text content into {len(chunks)} chunk(s)")
    return chunks
