"""Standalone script to ingest documents into the vector store.

Usage:
    python -m scripts.ingest
    python -m scripts.ingest --data-dir path/to/docs
"""

from __future__ import annotations

import argparse

from src.rag.ingestion import ingest
from src.rag.vector_store import add_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into the vector store.")
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Path to the directory containing documents to ingest (default: data/)",
    )
    args = parser.parse_args()

    print(f"Ingesting documents from '{args.data_dir}' ...")
    chunks = ingest(args.data_dir)
    if not chunks:
        print("No documents found. Place .txt or .pdf files in the data/ directory.")
        return

    add_documents(chunks)
    print(f"Successfully ingested {len(chunks)} chunks into the vector store.")


if __name__ == "__main__":
    main()
