# faiss_store.py

import faiss
import os
import pickle
import numpy as np
from app.core.config import settings

INDEX_PATH = settings.VECTOR_STORE_PATH
DOC_PATH = INDEX_PATH + "_docs.pkl"


def save_to_faiss(documents):
    embeddings = [doc["embedding"][0] for doc in documents]

    dim = len(embeddings[0])

    # Create index
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)

        with open(DOC_PATH, "rb") as f:
            stored_docs = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(dim)
        stored_docs = []

    # Add vectors
    index.add(np.array(embeddings))

    # Store docs
    stored_docs.extend(documents)

    # Save
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(DOC_PATH, "wb") as f:
        pickle.dump(stored_docs, f)


def load_vector_store():
    if not os.path.exists(INDEX_PATH):
        raise ValueError("Vector store not found. Upload documents first.")

    index = faiss.read_index(INDEX_PATH)

    with open(DOC_PATH, "rb") as f:
        documents = pickle.load(f)

    return index, documents