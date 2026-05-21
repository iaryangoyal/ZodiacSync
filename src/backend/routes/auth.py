import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from src.backend.dependencies import get_current_user
from src.backend.schemas.auth import TokenResponse, UserCreate, UserLogin, UserResponse
from src.backend.services.auth_service import (
    authenticate_user,
    build_token_response,
    create_user,
)
from src.config import get_optional_env

router = APIRouter(prefix="/auth", tags=["auth"])


def ensure_auth_configured() -> None:
    if not get_optional_env("JWT_SECRET_KEY"):
        raise HTTPException(status_code=503, detail="JWT_SECRET_KEY is not configured.")


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate):
    ensure_auth_configured()
    try:
        user = create_user(payload)
        return build_token_response(user)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="An account with this email already exists.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    ensure_auth_configured()
    user = authenticate_user(payload)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    try:
        return build_token_response(user)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    return current_user
