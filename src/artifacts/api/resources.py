from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import GatheringSkill
from ..models.pagination import DataPage
from ..models.resources import ResourceSchema

if TYPE_CHECKING:
    from ..http import HttpClient


class ResourcesAPI:
    """Resource endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        skill: Optional[GatheringSkill] = None,
        drop: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[ResourceSchema]:
        """GET /resources"""
        params = {
            "min_level": min_level,
            "max_level": max_level,
            "skill": skill,
            "drop": drop,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            "/resources", ResourceSchema, params=params
        )

    async def get(self, code: str) -> ResourceSchema:
        """GET /resources/{code}"""
        return await self._http.get_model(
            f"/resources/{code}", ResourceSchema
        )
