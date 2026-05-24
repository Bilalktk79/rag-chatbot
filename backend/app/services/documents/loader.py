# loader.py

import os


def load_text_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_text_file(file_path)

    # Future: PDF, DOCX
    else:
        raise ValueError(f"Unsupported file type: {ext}")