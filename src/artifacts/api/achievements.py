from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.achievements import AchievementSchema
from ..models.enums import AchievementType
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class AchievementsAPI:
    """Game achievements (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        type: Optional[AchievementType] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[AchievementSchema]:
        """GET /achievements"""
        params = {"type": type, "page": page, "size": size}
        return await self._http.get_page(
            "/achievements", AchievementSchema, params=params
        )

    async def get(self, code: str) -> AchievementSchema:
        """GET /achievements/{code}"""
        return await self._http.get_model(
            f"/achievements/{code}", AchievementSchema
        )
