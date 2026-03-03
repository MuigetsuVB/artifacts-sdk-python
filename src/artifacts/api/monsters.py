from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import MonsterType
from ..models.monsters import MonsterSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class MonstersAPI:
    """Monster endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        name: Optional[str] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        drop: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[MonsterSchema]:
        """GET /monsters"""
        params = {
            "name": name,
            "min_level": min_level,
            "max_level": max_level,
            "drop": drop,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            "/monsters", MonsterSchema, params=params
        )

    async def get(self, code: str) -> MonsterSchema:
        """GET /monsters/{code}"""
        return await self._http.get_model(f"/monsters/{code}", MonsterSchema)
