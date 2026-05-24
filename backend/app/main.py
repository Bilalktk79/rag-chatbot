from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔥 IMPORT ROUTES
from app.api import chat, documents, admin
from app.auth.routes import router as auth_router

# =========================
# 🚀 APP INIT
# =========================
app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0"
)

# =========================
# 🌐 CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ production me specific domain use karo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔐 AUTH ROUTES (FINAL)
# =========================
# 👉 FINAL URLs:
# /api/auth/signup
# /api/auth/login
# /api/auth/google
# /api/auth/facebook
# /api/auth/linkedin
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])


# =========================
# 🤖 CHAT ROUTES
# =========================
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


# =========================
# 📄 DOCUMENT ROUTES
# =========================
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])


# =========================
# 🛠 ADMIN ROUTES
# =========================
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


# =========================
# 🧪 HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"message": "🚀 RAG Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}