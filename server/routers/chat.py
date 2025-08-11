import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from services.llm_router import stream_response, get_response

router = APIRouter()


class ChatRequest(BaseModel):
    model: str = "gpt-4o"
    messages: list[dict]
    language: str = "en"


class ChatResponse(BaseModel):
    content: str
    model: str
    language: str


@router.post("/chat")
async def chat(request: ChatRequest):
    """non-streaming chat endpoint"""

    try:
        content = await get_response(
            model=request.model,
            messages=request.messages,
            language=request.language,
        )
        return ChatResponse(
            content=content,
            model=request.model,
            language=request.language,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """sse streaming chat endpoint"""

    async def event_generator():
        try:
            async for token in stream_response(
                model=request.model,
                messages=request.messages,
                language=request.language,
            ):
                yield {"data": json.dumps({"token": token})}
            yield {"data": json.dumps({"done": True})}
            except Exception as e:
            yield {"data": json.dumps({"error": str(e)})}
    
    return EventSourceResponse(event_generator())


