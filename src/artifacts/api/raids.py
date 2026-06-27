from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http import HttpClient


class RaidsAPI:
    """Raid endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        name: Optional[str] = None,
        active: Optional[bool] = None,
        page: int = 1,
        size: int = 50,
    ) -> dict[str, Any]:
        """GET /raids"""
        params = {"name": name, "active": active, "page": page, "size": size}
        return await self._http.get("/raids", params=params)

    async def get(self, code: str) -> dict[str, Any]:
        """GET /raids/{code}"""
        return await self._http.get(f"/raids/{code}")

    async def get_leaderboard(
        self, code: str, *, page: int = 1, size: int = 50
    ) -> dict[str, Any]:
        """GET /raids/{code}/leaderboard"""
        return await self._http.get(
            f"/raids/{code}/leaderboard",
            params={"page": page, "size": size},
        )
