from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.character import ActiveCharacterSchema, CharacterSchema
from ..models.enums import CharacterSkin
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class CharactersAPI:
    """Character management endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def create(self, name: str, skin: CharacterSkin) -> CharacterSchema:
        """POST /characters/create -- create a new character (max 5)."""
        return await self._http.post_model(
            "/characters/create",
            CharacterSchema,
            json={"name": name, "skin": skin},
        )

    async def delete(self, name: str) -> CharacterSchema:
        """POST /characters/delete -- delete a character."""
        return await self._http.post_model(
            "/characters/delete",
            CharacterSchema,
            json={"name": name},
        )

    async def get_active(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[ActiveCharacterSchema]:
        """GET /characters/active"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            "/characters/active", ActiveCharacterSchema, params=params
        )

    async def get(self, name: str) -> CharacterSchema:
        """GET /characters/{name}"""
        return await self._http.get_model(f"/characters/{name}", CharacterSchema)
