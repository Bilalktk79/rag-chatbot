# backend/app/api/admin.py

from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running "
    }


@router.get("/stats")
def stats():
    vector_store_path = "vector_store"

    num_files = len(os.listdir("data")) if os.path.exists("data") else 0
    vector_exists = os.path.exists(vector_store_path)

    return {
        "documents_uploaded": num_files,
        "vector_store_ready": vector_exists
    }