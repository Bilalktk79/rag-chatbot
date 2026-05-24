# memory_store.py

session_memory = {}


def get_session(session_id: str):
    return session_memory.get(session_id, [])


def save_session(session_id: str, data):
    session_memory[session_id] = data


def clear_session(session_id: str):
    if session_id in session_memory:
        del session_memory[session_id]