from collections.abc import AsyncIterator

import httpx

from app.config import settings


class OpenRouterClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.openrouter_base_url,
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        response = await self._client.post(
            "/chat/completions",
            json={"model": model or settings.openrouter_model, "messages": messages},
        )
        response.raise_for_status()
        return response.json()

    async def chat_stream(
        self, messages: list[dict], model: str | None = None
    ) -> AsyncIterator[str]:
        async with self._client.stream(
            "POST",
            "/chat/completions",
            json={
                "model": model or settings.openrouter_model,
                "messages": messages,
                "stream": True,
            },
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line + "\n\n"


openrouter = OpenRouterClient()
