from app.services.rag.retriever import retrieve_documents
from app.services.rag.generator import generate_answer
from app.services.memory.memory_service import get_chat_history, save_chat
from app.core.prompts import SYSTEM_PROMPT


def is_relevant(doc_content: str, query: str):
    query_words = query.lower().split()
    match_count = sum(1 for w in query_words if w in doc_content.lower())
    return match_count >= 2


def generate_response(query: str, session_id: str, history=None):
    # 1) history
    history = get_chat_history(session_id)

    # 🔥 DEBUG
    print("QUERY:", query)
    print("HISTORY:", history)

    # 2) retrieve
    docs = retrieve_documents(query)

    # 3) filter relevant
    relevant_docs = []
    for d in docs:
        if is_relevant(d["content"], query):
            relevant_docs.append(d)

    # 4) build context (if any)
    context_text = "\n".join([d["content"] for d in relevant_docs]) if relevant_docs else ""

    # 5) FLEXIBLE PROMPT
    prompt = f"""
You are an intelligent AI assistant.

Answer the user's question clearly and directly.

If context is useful, use it silently.
If context is not useful, ignore it completely.

DO NOT mention context.
DO NOT explain reasoning.

Question:
{query}
"""

    # 🔥 DEBUG PROMPT
    print("PROMPT DEBUG:\n", prompt)

    # 6) call LLM
    answer = generate_answer(prompt)

    # 🔥 DEBUG FINAL RESPONSE
    print("FINAL RESPONSE:", answer)

    # 7) sources
    sources = list(set([d["source"] for d in relevant_docs])) if relevant_docs else []

    # 8) save chat
    save_chat(session_id, query, answer)

    return {
        "answer": answer,
        "sources": sources
    }