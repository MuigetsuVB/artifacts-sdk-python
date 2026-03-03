from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.enums import XPType
from ..models.events import ActiveEventSchema
from ..models.sandbox import (
    SandboxGiveGoldDataSchema,
    SandboxGiveItemDataSchema,
    SandboxGiveXPDataSchema,
)

if TYPE_CHECKING:
    from ..http import HttpClient


class SandboxAPI:
    """Sandbox-only endpoints (for testing on sandbox server)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def give_gold(
        self, character: str, quantity: int
    ) -> SandboxGiveGoldDataSchema:
        """POST /sandbox/give_gold"""
        return await self._http.post_model(
            "/sandbox/give_gold",
            SandboxGiveGoldDataSchema,
            json={"character": character, "quantity": quantity},
        )

    async def give_item(
        self, character: str, code: str, quantity: int
    ) -> SandboxGiveItemDataSchema:
        """POST /sandbox/give_item"""
        return await self._http.post_model(
            "/sandbox/give_item",
            SandboxGiveItemDataSchema,
            json={"character": character, "code": code, "quantity": quantity},
        )

    async def give_xp(
        self, character: str, type: XPType, amount: int
    ) -> SandboxGiveXPDataSchema:
        """POST /sandbox/give_xp"""
        return await self._http.post_model(
            "/sandbox/give_xp",
            SandboxGiveXPDataSchema,
            json={"character": character, "type": type, "amount": amount},
        )

    async def spawn_event(self, code: str) -> ActiveEventSchema:
        """POST /sandbox/spawn_event"""
        return await self._http.post_model(
            "/sandbox/spawn_event",
            ActiveEventSchema,
            json={"code": code},
        )

    async def reset_account(self) -> str:
        """POST /sandbox/reset_account"""
        data = await self._http.post("/sandbox/reset_account")
        return data.get("message", "OK")
