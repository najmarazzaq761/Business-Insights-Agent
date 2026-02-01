import sqlite3
import uuid
import datetime
from langchain_community.chat_message_histories import SQLChatMessageHistory

from backend.config import CHAT_HISTORY_DB_PATH

DB_PATH = CHAT_HISTORY_DB_PATH

def ensure_tables():
    """Create the sessions table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_session(title: str = "New Chat") -> str:
    """Create a new chat session and return its ID."""
    ensure_tables()
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_sessions (id, title) VALUES (?, ?)", (session_id, title))
    conn.commit()
    conn.close()
    return session_id

def list_sessions():
    """Return a list of all chat sessions, ordered by creation time (newest first)."""
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM chat_sessions ORDER BY created_at DESC")
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sessions

def get_message_history(session_id: str):
    """Return the SQLChatMessageHistory object for a specific session."""
    # Note: SQLChatMessageHistory will automatically create the message_store table if needed.
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///" + DB_PATH
    )

def update_session_title(session_id: str, new_title: str):
    """Update the title of a specific session."""
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE chat_sessions SET title = ? WHERE id = ?", (new_title, session_id))
    conn.commit()
    conn.close()

def delete_session(session_id: str):
    """Delete a session from the sessions table and the message store."""
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
    
    try:
        cursor.execute("DELETE FROM message_store WHERE session_id = ?", (session_id,))
    except sqlite3.OperationalError:
   
        pass
    conn.commit()
    conn.close()
