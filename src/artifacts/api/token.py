from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp

if TYPE_CHECKING:
    from ..http import HttpClient


class TokenAPI:
    """POST /token -- generate a JWT from username/password."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def generate(self, username: str, password: str) -> str:
        """Generate a JWT token using HTTP Basic auth.

        Returns the token string.
        """
        auth = aiohttp.BasicAuth(username, password)
        data = await self._http.post("/token", auth=auth)
        return data["token"]
