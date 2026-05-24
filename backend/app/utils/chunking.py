# chunking.py

from app.core.config import settings


def chunk_text(text: str):
    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP

    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks