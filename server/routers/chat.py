import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from services.llm_router import stream_response, get_response

router = APIRouter()

class ChatRequest(BaseModel):
    model: str = "gpt-4o"
    messages: list[dict]
    language: str = "en"

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        async for token in stream_response(request.model, request.messages, request.language):
            yield {"data": json.dumps({"token": token})}
        yield {"data": json.dumps({"done": True})}
    return EventSourceResponse(event_generator())
