import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.backend.database import init_db
from src.backend.routes import auth, chat, health
from src.config import PROJECT_ROOT as CONFIG_PROJECT_ROOT, get_optional_env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database initialized.")
    yield


def get_cors_origins() -> list[str]:
    raw_origins = get_optional_env("BACKEND_CORS_ORIGINS", "")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app() -> FastAPI:
    app = FastAPI(
        title="ZodiacSync API",
        version="0.2.0",
        description="AI-Powered Vedic Astrology and Panchang API",
        lifespan=lifespan,
    )

    cors_origins = get_cors_origins()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=r"^http://(localhost|127\.0\.0\.1)(:\d+)?$" if not cors_origins else None,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {"message": "Welcome to ZodiacSync API"}

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(chat.router)

    frontend_dir = CONFIG_PROJECT_ROOT / "frontend"
    if frontend_dir.exists():
        app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.backend.main:app", host="127.0.0.1", port=8000)
