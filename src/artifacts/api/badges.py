from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.badges import BadgeSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class BadgesAPI:
    """Game badges (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[BadgeSchema]:
        """GET /badges"""
        params = {"page": page, "size": size}
        return await self._http.get_page("/badges", BadgeSchema, params=params)

    async def get(self, code: str) -> BadgeSchema:
        """GET /badges/{code}"""
        return await self._http.get_model(f"/badges/{code}", BadgeSchema)
