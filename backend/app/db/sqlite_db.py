import sqlite3

# DB connect
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# TABLE CREATE (auto run)
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    message TEXT
)
""")
conn.commit()


# ✅ SAVE MESSAGE
def save_message(session_id, role, message):
    cursor.execute(
        "INSERT INTO chats (session_id, role, message) VALUES (?, ?, ?)",
        (session_id, role, message)
    )
    conn.commit()


# ✅ GET HISTORY
def get_history(session_id):
    cursor.execute(
        "SELECT role, message FROM chats WHERE session_id=? ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()

    # format for LLM
    history = []
    for role, message in rows:
        history.append({
            "role": role,
            "content": message
        })

    return history


# ✅ GET ALL SESSIONS (sidebar ke liye)
def get_sessions():
    cursor.execute("SELECT DISTINCT session_id FROM chats")
    rows = cursor.fetchall()
    return [r[0] for r in rows]