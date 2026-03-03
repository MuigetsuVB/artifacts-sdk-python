from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import NPCType
from ..models.npcs import NPCItem, NPCSchema
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
        page: int = 1,
        size: int = 50,
    ) -> DataPage[NPCSchema]:
        """GET /npcs/details"""
        params = {"name": name, "type": type, "page": page, "size": size}
        return await self._http.get_page(
            "/npcs/details", NPCSchema, params=params
        )

    async def get(self, code: str) -> NPCSchema:
        """GET /npcs/details/{code}"""
        return await self._http.get_model(f"/npcs/details/{code}", NPCSchema)

    async def get_all_items(
        self,
        *,
        code: Optional[str] = None,
        npc: Optional[str] = None,
        currency: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[NPCItem]:
        """GET /npcs/items"""
        params = {
            "code": code,
            "npc": npc,
            "currency": currency,
            "page": page,
            "size": size,
        }
        return await self._http.get_page("/npcs/items", NPCItem, params=params)

    async def get_items(
        self,
        code: str,
        *,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[NPCItem]:
        """GET /npcs/items/{code}"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            f"/npcs/items/{code}", NPCItem, params=params
        )
