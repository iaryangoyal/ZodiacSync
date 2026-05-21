from fastapi import APIRouter

from src.ai_engine.knowledge.store import is_knowledge_store_available
from src.backend.database import get_database_path
from src.backend.schemas.health import HealthResponse
from src.config import get_optional_env

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "ai_configured": bool(get_optional_env("OPENAI_API_KEY")),
        "auth_configured": bool(get_optional_env("JWT_SECRET_KEY")),
        "database_configured": bool(get_database_path()),
        "knowledge_store_available": is_knowledge_store_available(),
    }
