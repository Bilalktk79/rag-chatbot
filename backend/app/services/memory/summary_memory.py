# summary_memory.py

from app.services.rag.generator import generate_answer

summary_store = {}


def summarize_history(session_id: str, full_history: str):
    prompt = f"""
Summarize the following conversation in a concise way:

{full_history}
"""

    summary = generate_answer(prompt)

    summary_store[session_id] = summary

    return summary


def get_summary(session_id: str):
    return summary_store.get(session_id, "")