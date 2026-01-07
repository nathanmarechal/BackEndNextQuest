from fastapi import APIRouter, HTTPException
from schemas.schema import AssistantChatRequest, AssistantChatResponse
from services.assistant_provider import get_assistant_provider

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/chat", response_model=AssistantChatResponse)
async def chat(req: AssistantChatRequest):
    msg = (req.message or "").strip()
    if not msg:
        raise HTTPException(status_code=400, detail="message is required")

    provider = get_assistant_provider()
    result = await provider.chat(
        message=msg,
    )

    return AssistantChatResponse(**result)