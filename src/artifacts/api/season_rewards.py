from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..http import HttpClient


class SeasonRewardsAPI:
    """Season reward endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        type: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> dict[str, Any]:
        """GET /season_rewards"""
        return await self._http.get(
            "/season_rewards",
            params={"type": type, "page": page, "size": size},
        )

    async def get(self, code: str, *, page: int = 1, size: int = 50) -> dict[str, Any]:
        """GET /season_rewards/{code}"""
        return await self._http.get(
            f"/season_rewards/{code}",
            params={"page": page, "size": size},
        )
