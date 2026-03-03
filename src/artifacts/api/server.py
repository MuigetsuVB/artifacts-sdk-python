from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.server import StatusSchema

if TYPE_CHECKING:
    from ..http import HttpClient


class ServerAPI:
    """GET / -- game server status."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_status(self) -> StatusSchema:
        """Return the status of the game server."""
        return await self._http.get_model("/", StatusSchema)
