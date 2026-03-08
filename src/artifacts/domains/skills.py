"""Skills domain -- gathering, crafting, recycling."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.responses import RecyclingDataSchema, SkillDataSchema
from ._base import CharacterDomain


class SkillsDomain(CharacterDomain):
    """Manage skill actions (gathering, crafting, recycling).

    Accessed via ``character.skills``::

        await char.skills.gather()
        await char.skills.craft(code="iron_sword", quantity=2)
        await char.skills.recycle(code="wooden_shield")
    """

    @_auto_cooldown
    async def gather(self) -> SkillDataSchema:
        """Gather a resource at the current map location."""
        return await self._http.post_model(
            f"{self._base}/gathering", SkillDataSchema
        )

    @_auto_cooldown
    async def craft(self, *, code: str, quantity: int = 1) -> SkillDataSchema:
        """Craft an item."""
        return await self._http.post_model(
            f"{self._base}/crafting",
            SkillDataSchema,
            json={"code": code, "quantity": quantity},
        )

    @_auto_cooldown
    async def recycle(self, *, code: str, quantity: int = 1) -> RecyclingDataSchema:
        """Recycle an item into materials."""
        return await self._http.post_model(
            f"{self._base}/recycling",
            RecyclingDataSchema,
            json={"code": code, "quantity": quantity},
        )
