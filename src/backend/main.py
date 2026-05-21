import logging
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.ai_engine.knowledge.store import retrieve_context
from src.ai_engine.ai_service import generate_response
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None


MAX_HISTORY_MESSAGES = 20
chat_history_store: dict[str, list[dict[str, str]]] = defaultdict(list)



app = FastAPI(
    title="ZodiacSync API",
    version="0.1.0",
    description="AI-Powered Vedic Astrology and Panchang API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "🪔 Welcome to ZodiacSync API — AI Pandit is alive!"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest, request: Request):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    client_host = request.client.host if request.client else "anonymous"
    user_id = req.user_id or client_host
    history = chat_history_store[user_id]

    try:
        # 🔍 retrieve knowledge
        context = retrieve_context(message)

        # 🤖 generate response
        response = generate_response(
            query=message,
            context=context,
            history=history
        )

        # 💾 store chat
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        del history[:-MAX_HISTORY_MESSAGES]

        return {"response": response}
    except Exception as exc:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.backend.main:app", host="127.0.0.1", port=8000)
