from fastapi import APIRouter
from pydantic import BaseModel

from services.rag_service import ask_question


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(
    request: ChatRequest
):

    result = ask_question(
        request.question
    )

    return result