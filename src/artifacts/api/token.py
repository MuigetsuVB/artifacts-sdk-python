from __future__ import annotations

from typing import TYPE_CHECKING

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
        data = await self._http.post("/token", auth=(username, password))
        return data["token"]
