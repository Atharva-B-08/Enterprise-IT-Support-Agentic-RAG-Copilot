import time

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import get_settings

settings = get_settings()


_embeddings = None
_vectorstore = None

# Output size of each embedding model. The Pinecone index must match this exactly.
EMBEDDING_DIMENSIONS = {
    "gemini-embedding-001": 3072,
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
    "all-minilm-l6-v2": 384,
}


def _normalized_model_name(model_name: str | None = None) -> str:
    name = (model_name or settings.embedding_model or "").strip().lower()
    if not name:
        raise ValueError("Model name is required to get embedding dimensions.")
    return name.removeprefix("models/")


def get_embeddings_dimension(model_name: str | None = None) -> int:
    name = _normalized_model_name(model_name)
    if name in EMBEDDING_DIMENSIONS:
        return EMBEDDING_DIMENSIONS[name]
    raise ValueError(
        f"Unsupported embedding model '{name}' for Pinecone. "
        "Add the matching dimension to EMBEDDING_DIMENSIONS."
    )


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        if not settings.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is missing")
        # embed_documents() uses the retrieval-document task type and embed_query()
        # uses the retrieval-query task type automatically.
        _embeddings = GoogleGenerativeAIEmbeddings(
            model=f"models/{_normalized_model_name()}",
            google_api_key=settings.google_api_key,
        )
    return _embeddings


def ensure_index():
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is missing")

    desired_dimension = get_embeddings_dimension()
    pc = Pinecone(api_key=settings.pinecone_api_key)
    names = [x["name"] for x in pc.list_indexes()]

    if settings.pinecone_index_name in names:
        index_info = pc.describe_index(settings.pinecone_index_name)
        current_dimension = getattr(index_info, "dimension", None)
        if current_dimension is None and isinstance(index_info, dict):
            current_dimension = index_info.get("dimension")

        # An index cannot change dimension, so a mismatch means it was built for a
        # different embedding model. Recreate it (development behaviour).
        if current_dimension is not None and current_dimension != desired_dimension:
            print(
                f"Index '{settings.pinecone_index_name}' has dimension {current_dimension}, "
                f"expected {desired_dimension}. Recreating it."
            )
            pc.delete_index(name=settings.pinecone_index_name)
            while settings.pinecone_index_name in [x["name"] for x in pc.list_indexes()]:
                time.sleep(1)

    if settings.pinecone_index_name not in [x["name"] for x in pc.list_indexes()]:
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=desired_dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(settings.pinecone_index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(settings.pinecone_index_name)


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        index = ensure_index()
        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=get_embeddings(),
            namespace=settings.pinecone_namespace,
        )
    return _vectorstore


def get_retriever():
    # Never retrieve chunks from documents marked `status: superseded` (e.g. the 2024 quick tips).
    return get_vectorstore().as_retriever(
        search_kwargs={
            "k": settings.top_k,
            "filter": {"status": {"$ne": "superseded"}},
        }
    )


def _is_rate_limit(error: Exception) -> bool:
    text = str(error)
    return "429" in text or "RESOURCE_EXHAUSTED" in text or "rate" in text.lower()


def add_documents(chunks, ids=None, batch_size: int = 40):
    """Embed and upsert chunks in small batches, retrying when the free tier rate-limits."""
    store = get_vectorstore()
    total = 0
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        batch_ids = ids[start:start + batch_size] if ids else None
        for attempt in range(5):
            try:
                store.add_documents(batch, ids=batch_ids)
                break
            except Exception as error:
                if attempt == 4 or not _is_rate_limit(error):
                    raise
                wait = 20 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s before retrying...")
                time.sleep(wait)
        total += len(batch)
        print(f"  Upserted {total}/{len(chunks)}")
        time.sleep(1)
    return total
