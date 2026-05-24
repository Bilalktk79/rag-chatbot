# processor.py

from app.services.documents.loader import load_document
from app.utils.chunking import chunk_text
from app.services.embeddings.embedder import get_embedding
from app.db.vector.faiss_store import save_to_faiss


def process_document(file_path: str):
    # 📄 1. Load document
    text = load_document(file_path)

    # ✂️ 2. Chunk text
    chunks = chunk_text(text)

    documents = []

    # 🧠 3. Create embeddings
    for chunk in chunks:
        embedding = get_embedding(chunk)

        documents.append({
            "content": chunk,
            "embedding": embedding,
            "source": file_path
        })

    # 💾 4. Store in FAISS
    save_to_faiss(documents)