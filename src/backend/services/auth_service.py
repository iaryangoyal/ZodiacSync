import sqlite3

from src.backend.database import get_db
from src.backend.schemas.auth import UserCreate, UserLogin
from src.backend.security import create_access_token, hash_password, verify_password


def row_to_user(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "email": row["email"],
        "full_name": row["full_name"],
    }


def get_user_by_id(user_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, email, full_name FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return row_to_user(row) if row else None


def get_user_by_email(email: str) -> sqlite3.Row | None:
    with get_db() as conn:
        return conn.execute(
            "SELECT id, email, full_name, hashed_password FROM users WHERE email = ?",
            (email,),
        ).fetchone()


def create_user(payload: UserCreate) -> dict:
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO users (email, full_name, hashed_password)
            VALUES (?, ?, ?)
            """,
            (payload.email, payload.full_name, hash_password(payload.password)),
        )
        user_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, email, full_name FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return row_to_user(row)


def authenticate_user(payload: UserLogin) -> dict | None:
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        return None

    return row_to_user(user)


def build_token_response(user: dict) -> dict:
    return {
        "access_token": create_access_token(str(user["id"])),
        "token_type": "bearer",
        "user": user,
    }
