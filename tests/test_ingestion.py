"""Tests for the document ingestion pipeline."""

from langchain_core.documents import Document

from src.rag.ingestion import split_documents


def test_split_documents_produces_chunks():
    """Splitting a long document should produce multiple chunks."""
    long_text = "word " * 500  # ~2500 chars
    docs = [Document(page_content=long_text, metadata={"source": "test"})]
    chunks = split_documents(docs)
    assert len(chunks) > 1


def test_split_documents_empty_input():
    """Splitting an empty list should return an empty list."""
    assert split_documents([]) == []
