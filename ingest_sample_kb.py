"""Ingest the sample IT knowledge base (data/sample_kb) into Pinecone.

Run from the project root:
    uv run python ingest_sample_kb.py            # upsert (safe to re-run, ids are stable)
    uv run python ingest_sample_kb.py --reset    # wipe the namespace first
    uv run python ingest_sample_kb.py --dry-run  # chunk only, no API calls
"""
import argparse
from collections import Counter
from pathlib import Path

from app.core.config import get_settings
from app.rag.chunking import load_kb_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest the sample KB into Pinecone.")
    parser.add_argument("--reset", action="store_true", help="delete all vectors in the namespace first")
    parser.add_argument("--dry-run", action="store_true", help="chunk and report, without calling any API")
    args = parser.parse_args()

    settings = get_settings()
    kb_dir = Path(settings.sample_kb_dir)
    chunks = load_kb_chunks(kb_dir)
    if not chunks:
        raise SystemExit(f"No chunks found under {kb_dir}")

    types = Counter(c.metadata["type"] for c in chunks)
    statuses = Counter(c.metadata["status"] for c in chunks)
    print(f"Loaded {len(chunks)} chunks from {kb_dir}")
    print(f"  by type:   {dict(types)}")
    print(f"  by status: {dict(statuses)} (superseded chunks are stored but filtered out at query time)")

    if args.dry_run:
        return

    # Imported here so --dry-run works without any API keys configured.
    from app.rag.vectorstore import add_documents, get_vectorstore

    if args.reset:
        try:
            get_vectorstore().delete(delete_all=True)
            print(f"Cleared namespace '{settings.pinecone_namespace}'")
        except Exception as error:  # an empty or new namespace can raise "not found"
            print(f"Nothing to clear ({error})")

    ids = [c.metadata["chunk_id"] for c in chunks]
    total = add_documents(chunks, ids=ids)
    print(f"Done. {total} chunks in index '{settings.pinecone_index_name}', "
          f"namespace '{settings.pinecone_namespace}'.")


if __name__ == "__main__":
    main()
