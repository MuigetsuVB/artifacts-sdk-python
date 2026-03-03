from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import MapContentType, MapLayer
from ..models.maps import MapSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class MapsAPI:
    """Map endpoints (public, no auth)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_all(
        self,
        *,
        layer: Optional[MapLayer] = None,
        content_type: Optional[MapContentType] = None,
        content_code: Optional[str] = None,
        hide_blocked_maps: Optional[bool] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[MapSchema]:
        """GET /maps"""
        params = {
            "layer": layer,
            "content_type": content_type,
            "content_code": content_code,
            "hide_blocked_maps": hide_blocked_maps,
            "page": page,
            "size": size,
        }
        return await self._http.get_page("/maps", MapSchema, params=params)

    async def get_layer(
        self,
        layer: MapLayer,
        *,
        content_type: Optional[MapContentType] = None,
        content_code: Optional[str] = None,
        hide_blocked_maps: Optional[bool] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[MapSchema]:
        """GET /maps/{layer}"""
        params = {
            "content_type": content_type,
            "content_code": content_code,
            "hide_blocked_maps": hide_blocked_maps,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            f"/maps/{layer}", MapSchema, params=params
        )

    async def get_by_position(
        self, layer: MapLayer, x: int, y: int
    ) -> MapSchema:
        """GET /maps/{layer}/{x}/{y}"""
        return await self._http.get_model(
            f"/maps/{layer}/{x}/{y}", MapSchema
        )

    async def get_by_id(self, map_id: int) -> MapSchema:
        """GET /maps/id/{map_id}"""
        return await self._http.get_model(f"/maps/id/{map_id}", MapSchema)
