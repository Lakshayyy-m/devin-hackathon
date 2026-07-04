from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.openrouter import openrouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await openrouter.close()


app = FastAPI(title="Hackathon API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict:
    if not settings.openrouter_api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY is not set")
    messages = [m.model_dump() for m in request.messages]
    result = await openrouter.chat(messages, request.model)
    return {
        "message": result["choices"][0]["message"],
        "model": result.get("model"),
        "usage": result.get("usage"),
    }


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    if not settings.openrouter_api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY is not set")
    messages = [m.model_dump() for m in request.messages]
    return StreamingResponse(
        openrouter.chat_stream(messages, request.model),
        media_type="text/event-stream",
    )
