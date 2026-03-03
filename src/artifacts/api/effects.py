from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.effects import EffectSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class EffectsAPI:
    """Game effects (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[EffectSchema]:
        """GET /effects"""
        params = {"page": page, "size": size}
        return await self._http.get_page("/effects", EffectSchema, params=params)

    async def get(self, code: str) -> EffectSchema:
        """GET /effects/{code}"""
        return await self._http.get_model(f"/effects/{code}", EffectSchema)
