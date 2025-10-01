from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import chat, voice

app = FastAPI(title="LoquiAI", version="1.0.0")

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(chat.router, prefix="/api")
app.include_router(voice.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "loqui-ai"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
