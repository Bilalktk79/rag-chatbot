# buffer_memory.py

from app.core.config import settings

# In-memory store (later Redis upgrade possible)
memory_store = {}


def get_buffer_memory(session_id: str):
    return memory_store.get(session_id, [])


def add_to_buffer(session_id: str, user_query: str, bot_response: str):
    if session_id not in memory_store:
        memory_store[session_id] = []

    memory_store[session_id].append({
        "user": user_query,
        "bot": bot_response
    })

    # Keep only last N messages
    if len(memory_store[session_id]) > settings.MAX_HISTORY:
        memory_store[session_id] = memory_store[session_id][-settings.MAX_HISTORY:]


def format_buffer_history(session_id: str):
    history = get_buffer_memory(session_id)

    formatted = ""
    for chat in history:
        formatted += f"User: {chat['user']}\nAssistant: {chat['bot']}\n"

    return formatted