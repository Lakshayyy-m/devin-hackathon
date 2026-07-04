# Hackathon App

Boilerplate: TanStack Start (React) frontend + FastAPI backend with OpenRouter AI integration.

## Structure

- `frontend/` — TanStack Start + React + Tailwind (Vite, port 3000)
- `backend/` — FastAPI + OpenRouter client (uvicorn, port 8000)

## Quick start

### Backend

```bash
cd backend
cp .env.example .env   # add your OPENROUTER_API_KEY
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Get an OpenRouter API key at https://openrouter.ai/keys.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 — the dev server proxies `/api/*` to the backend.

## API

- `GET /api/health` — health check
- `POST /api/chat` — `{ "messages": [{"role": "user", "content": "hi"}], "model": "optional/override" }`
- `POST /api/chat/stream` — same body, SSE streaming response

Default model is set via `OPENROUTER_MODEL` in `backend/.env` (see `backend/.env.example`).
