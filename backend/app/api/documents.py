# backend/app/api/documents.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid

from app.services.documents.processor import process_document

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ ALLOWED TYPES
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}

# ✅ MAX SIZE (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # =========================
        # 🔍 VALIDATE FILE TYPE
        # =========================
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOC, DOCX, TXT allowed"
            )

        # =========================
        # 🔍 VALIDATE FILE SIZE
        # =========================
        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large (max 10MB)"
            )

        # =========================
        # 🔥 UNIQUE FILE NAME
        # =========================
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        # =========================
        # 💾 SAVE FILE
        # =========================
        with open(file_path, "wb") as f:
            f.write(contents)

        # =========================
        # 🧠 PROCESS (RAG PIPELINE)
        # =========================
        process_document(file_path)

        return {
            "status": "success",
            "filename": filename,
            "stored_as": unique_name
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }