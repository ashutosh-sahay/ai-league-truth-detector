"""Document ingestion – load, split, and prepare documents for embedding."""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
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

    # Load PDF files
    pdf_loader = DirectoryLoader(
        str(data_path), glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True
    )
    documents.extend(pdf_loader.load())

    logger.info(f"Loaded {len(documents)} document(s) from '{data_path}'.")
    return documents


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
