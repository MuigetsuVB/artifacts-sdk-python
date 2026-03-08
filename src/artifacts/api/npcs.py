from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import NPCType
from ..models.npcs import NPCSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class NPCsAPI:
    """NPC endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        name: Optional[str] = None,
        type: Optional[NPCType] = None,
        currency: Optional[str] = None,
        item: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[NPCSchema]:
        """GET /npcs/details"""
        params = {
            "name": name,
            "type": type,
            "currency": currency,
            "item": item,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            "/npcs/details", NPCSchema, params=params
        )

    async def get(self, code: str) -> NPCSchema:
        """GET /npcs/details/{code}"""
        return await self._http.get_model(f"/npcs/details/{code}", NPCSchema)
