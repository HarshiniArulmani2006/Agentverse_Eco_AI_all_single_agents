"""
WildGuard AI – Chat Router
Main conversational endpoint with RAG and session memory.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from core.gemini_client import gemini
from core.memory import memory
from services.rag_service import retrieve_context

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    rag_context_used: bool
    history_length: int


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Main chat endpoint with RAG and session memory."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Get or create session
    session_id = req.session_id or memory.new_session()
    memory.get_or_create(session_id)

    # RAG: retrieve relevant knowledge
    rag_context = retrieve_context(req.message)
    rag_used = bool(rag_context)

    # Build Gemini history from session
    history = memory.get_history_for_gemini(session_id)
    # Remove last message (will be added as current)
    gemini_history = history[:-1] if history else []

    # Generate response
    response_text = gemini.chat(
        message=req.message,
        history=gemini_history,
        rag_context=rag_context,
    )

    # Store exchange in memory
    memory.add_exchange(session_id, "user", req.message)
    memory.add_exchange(session_id, "assistant", response_text)

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        rag_context_used=rag_used,
        history_length=len(memory.get_history(session_id)),
    )


@router.delete("/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    memory.clear(session_id)
    return {"message": "Session cleared", "session_id": session_id}


@router.get("/{session_id}/history")
async def get_history(session_id: str):
    """Get conversation history for a session."""
    return {
        "session_id": session_id,
        "history": memory.get_history(session_id),
    }
