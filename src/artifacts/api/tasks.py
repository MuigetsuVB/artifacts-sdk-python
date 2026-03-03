from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import Skill, TaskType
from ..models.monsters import DropRateSchema
from ..models.pagination import DataPage
from ..models.tasks import TaskFullSchema

if TYPE_CHECKING:
    from ..http import HttpClient


class TasksAPI:
    """Task game-data endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        skill: Optional[Skill] = None,
        type: Optional[TaskType] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[TaskFullSchema]:
        """GET /tasks/list"""
        params = {
            "min_level": min_level,
            "max_level": max_level,
            "skill": skill,
            "type": type,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            "/tasks/list", TaskFullSchema, params=params
        )

    async def get(self, code: str) -> TaskFullSchema:
        """GET /tasks/list/{code}"""
        return await self._http.get_model(
            f"/tasks/list/{code}", TaskFullSchema
        )

    async def get_all_rewards(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[DropRateSchema]:
        """GET /tasks/rewards"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            "/tasks/rewards", DropRateSchema, params=params
        )

    async def get_reward(self, code: str) -> DropRateSchema:
        """GET /tasks/rewards/{code}"""
        return await self._http.get_model(
            f"/tasks/rewards/{code}", DropRateSchema
        )
