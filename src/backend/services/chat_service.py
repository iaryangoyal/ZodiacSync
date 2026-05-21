from src.backend.database import get_db

MAX_HISTORY_MESSAGES = 20


def create_session(user_id: int, first_message: str) -> int:
    title = first_message[:48] or "New chat"
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO chat_sessions (user_id, title) VALUES (?, ?)",
            (user_id, title),
        )
        return int(cursor.lastrowid)


def get_user_session(user_id: int, session_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM chat_sessions
            WHERE id = ? AND user_id = ?
            """,
            (session_id, user_id),
        ).fetchone()

    return dict(row) if row else None


def list_sessions(user_id: int) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM chat_sessions
            WHERE user_id = ?
            ORDER BY updated_at DESC
            """,
            (user_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_recent_history(session_id: int) -> list[dict[str, str]]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, MAX_HISTORY_MESSAGES),
        ).fetchall()

    return [dict(row) for row in reversed(rows)]


def list_messages(user_id: int, session_id: int) -> list[dict[str, str]]:
    if not get_user_session(user_id, session_id):
        return []

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY id ASC
            """,
            (session_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def save_turn(session_id: int, user_message: str, assistant_response: str) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, 'user', ?)",
            (session_id, user_message),
        )
        conn.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, 'assistant', ?)",
            (session_id, assistant_response),
        )
        conn.execute(
            "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (session_id,),
        )
