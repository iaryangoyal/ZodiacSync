import logging

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAIError

from src.ai_engine.ai_service import generate_response
from src.ai_engine.knowledge.store import retrieve_context
from src.backend.dependencies import get_current_user
from src.backend.schemas.chat import ChatMessageResponse, ChatRequest, ChatResponse, ChatSessionResponse
from src.backend.services.chat_service import (
    create_session,
    get_recent_history,
    get_user_session,
    list_messages,
    list_sessions,
    save_turn,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/sessions", response_model=list[ChatSessionResponse])
def sessions(current_user: dict = Depends(get_current_user)):
    return list_sessions(current_user["id"])


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageResponse])
def messages(session_id: int, current_user: dict = Depends(get_current_user)):
    if not get_user_session(current_user["id"], session_id):
        raise HTTPException(status_code=404, detail="Chat session not found.")

    return list_messages(current_user["id"], session_id)


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, current_user: dict = Depends(get_current_user)):
    session_id = payload.session_id
    if session_id is None:
        session_id = create_session(current_user["id"], payload.message)
    elif not get_user_session(current_user["id"], session_id):
        raise HTTPException(status_code=404, detail="Chat session not found.")

    history = get_recent_history(session_id)

    try:
        context = retrieve_context(payload.message)
        response = generate_response(
            query=payload.message,
            context=context,
            history=history,
        )
        save_turn(session_id, payload.message, response)
        return {"response": response, "session_id": session_id}
    except OpenAIError as exc:
        logger.exception("OpenAI request failed")
        raise HTTPException(
            status_code=502,
            detail="AI service request failed. Please try again shortly.",
        ) from exc
    except RuntimeError as exc:
        logger.exception("Chat service is not ready")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later.",
        ) from exc
