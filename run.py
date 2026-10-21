from app.rag.vectorstore import add_documents
from app.services.ingestion import load_file, chunk_documents
from pathlib import Path

docs = load_file(Path("data/sample_kb/it-handbook.md"))
chunks = chunk_documents(docs)
print(len(chunks))  # 20 chunks

# add_documents(chunks)