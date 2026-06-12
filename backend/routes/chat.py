from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from services.rag_service import ask_question


router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    history: List[dict] = []


@router.post("/chat")
def chat(
    request: ChatRequest
):

    result = ask_question(
    request.question,
    request.history
    )

    return result