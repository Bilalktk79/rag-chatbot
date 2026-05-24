# retriever.py

from app.db.vector.faiss_store import load_vector_store
from app.services.embeddings.embedder import get_embedding
from app.core.config import settings


def retrieve_documents(query: str):
    index, documents = load_vector_store()

    query_vector = get_embedding(query)

    # 🔎 Search top-k similar docs
    distances, indices = index.search(query_vector, settings.TOP_K)

    results = []

    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results