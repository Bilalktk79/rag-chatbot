# memory_service.py

from app.services.memory.buffer_memory import (
    add_to_buffer,
    format_buffer_history
)

from app.services.memory.summary_memory import (
    summarize_history,
    get_summary
)


def get_chat_history(session_id: str):
    # Buffer history
    buffer_history = format_buffer_history(session_id)

    # Summary (optional)
    summary = get_summary(session_id)

    # Combine both
    return f"{summary}\n{buffer_history}"


def save_chat(session_id: str, user_query: str, bot_response: str):
    add_to_buffer(session_id, user_query, bot_response)

    # Optional: summarize if too long
    history = format_buffer_history(session_id)

    if len(history) > 1000:  # threshold
        summarize_history(session_id, history)