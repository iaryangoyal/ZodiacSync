from fastapi import FastAPI
import os
from pydantic import BaseModel
from src.ai_engine.knowledge.store import retrieve_context
from src.ai_engine.ai_service import generate_response

class ChatRequest(BaseModel):
    message: str

chat_history_store = {}



app = FastAPI(
    title="ZodiacSync API",
    version="0.1.0",
    description="AI-Powered Vedic Astrology and Panchang API"
)

@app.get("/")
def root():
    return {"message": "🪔 Welcome to ZodiacSync API — AI Pandit is alive!"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    user_id = "dev_user"

    if user_id not in chat_history_store:
        chat_history_store[user_id] = []

    history = chat_history_store[user_id]
    print(history)
    # 🔍 retrieve knowledge
    context = retrieve_context(req.message)

    # 🤖 generate response
    response = generate_response(
        query=req.message,
        context=context,
        history=history
    )

    # 💾 store chat
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": response})

    return {"response": response}