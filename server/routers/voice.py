from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.tts_service import synthesize_speech, get_supported_languages
import io

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    language: str = "en"


@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    """convert text to speech using aws polly"""
    try:
        audio_bytes = synthesize_speech(request.text, request.language)
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tts/languages")
async def supported_languages():
    return {"languages": get_supported_languages()}
