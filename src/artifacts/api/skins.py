from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http import HttpClient


class SkinsAPI:
    """Skin endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(self, *, page: int = 1, size: int = 50) -> dict[str, Any]:
        """GET /skins"""
        return await self._http.get("/skins", params={"page": page, "size": size})

    async def get(self, code: str) -> dict[str, Any]:
        """GET /skins/{code}"""
        return await self._http.get(f"/skins/{code}")
