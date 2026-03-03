from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.events import ActiveEventSchema, EventSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class EventsAPI:
    """Game events."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all_active(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[ActiveEventSchema]:
        """GET /events/active"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            "/events/active", ActiveEventSchema, params=params
        )

    async def get_all(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[EventSchema]:
        """GET /events"""
        params = {"page": page, "size": size}
        return await self._http.get_page("/events", EventSchema, params=params)

    async def spawn(self, code: str) -> ActiveEventSchema:
        """POST /events/spawn -- spawn an event (member/founder required)."""
        return await self._http.post_model(
            "/events/spawn", ActiveEventSchema, json={"code": code}
        )
