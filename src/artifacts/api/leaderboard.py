from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import AccountLeaderboardType, CharacterLeaderboardType
from ..models.leaderboard import AccountLeaderboardSchema, CharacterLeaderboardSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class LeaderboardAPI:
    """Leaderboard endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_characters(
        self,
        *,
        sort: Optional[CharacterLeaderboardType] = None,
        name: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[CharacterLeaderboardSchema]:
        """GET /leaderboard/characters"""
        params = {"sort": sort, "name": name, "page": page, "size": size}
        return await self._http.get_page(
            "/leaderboard/characters",
            CharacterLeaderboardSchema,
            params=params,
        )

    async def get_accounts(
        self,
        *,
        sort: Optional[AccountLeaderboardType] = None,
        name: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[AccountLeaderboardSchema]:
        """GET /leaderboard/accounts"""
        params = {"sort": sort, "name": name, "page": page, "size": size}
        return await self._http.get_page(
            "/leaderboard/accounts",
            AccountLeaderboardSchema,
            params=params,
        )
