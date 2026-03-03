from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import CraftSkill, ItemType
from ..models.items import ItemSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class ItemsAPI:
    """Game items (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        name: Optional[str] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        type: Optional[ItemType] = None,
        craft_skill: Optional[CraftSkill] = None,
        craft_material: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[ItemSchema]:
        """GET /items"""
        params = {
            "name": name,
            "min_level": min_level,
            "max_level": max_level,
            "type": type,
            "craft_skill": craft_skill,
            "craft_material": craft_material,
            "page": page,
            "size": size,
        }
        return await self._http.get_page("/items", ItemSchema, params=params)

    async def get(self, code: str) -> ItemSchema:
        """GET /items/{code}"""
        return await self._http.get_model(f"/items/{code}", ItemSchema)
