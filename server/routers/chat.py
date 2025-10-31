import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from services.llm_router import stream_response, get_response
from services.analytics import analytics

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
    analytics.on_request(model=request.model, language=request.language)

    try:
        content = await get_response(
            model=request.model,
            messages=request.messages,
            language=request.language,
        )
        analytics.on_success(model=request.model)
        return ChatResponse(
            content=content,
            model=request.model,
            language=request.language,
        )
    except Exception as e:
        analytics.on_error(model=request.model)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """sse streaming chat endpoint"""
    analytics.on_request(model=request.model, language=request.language)

    async def event_generator():
        try:
            async for token in stream_response(
                model=request.model,
                messages=request.messages,
                language=request.language,
            ):
                yield {"data": json.dumps({"token": token})}
            yield {"data": json.dumps({"done": True})}
            analytics.on_success(model=request.model)
        except Exception as e:
            yield {"data": json.dumps({"error": str(e)})}
            analytics.on_error(model=request.model)

    return EventSourceResponse(event_generator())


@router.get("/analytics")
async def get_analytics():
    return analytics.get_summary()
