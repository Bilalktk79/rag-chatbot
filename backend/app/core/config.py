import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 🔐 API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    # 🤖 Model Config
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.0-flash")
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 1024

    # 📂 Paths
    DATA_PATH: str = "data"
    VECTOR_STORE_PATH: str = "vector_store/faiss_index"

    # 🔎 Retrieval Config
    TOP_K: int = 3

    # 🧠 Chunking Config
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100

    # 🧠 Memory Config
    MAX_HISTORY: int = 5


# Singleton instance
settings = Settings()