from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http import HttpClient


class GameAssistantAPI:
    """Game assistant endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def ask(self, question: str) -> dict[str, Any]:
        """POST /game_assistant/ask"""
        return await self._http.post(
            "/game_assistant/ask",
            json={"question": question},
        )
