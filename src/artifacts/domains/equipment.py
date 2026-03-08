"""Equipment domain -- equip and unequip items."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.enums import ItemSlot
from ..models.responses import EquipRequestSchema
from ._base import CharacterDomain


class EquipmentDomain(CharacterDomain):
    """Manage character equipment.

    Accessed via ``character.equipment``::

        await char.equipment.equip(code="iron_sword", slot=ItemSlot.WEAPON)
        await char.equipment.unequip(slot=ItemSlot.HELMET)
    """

    @_auto_cooldown
    async def equip(
        self, *, code: str, slot: ItemSlot, quantity: int = 1
    ) -> EquipRequestSchema:
        """Equip an item into a slot."""
        return await self._http.post_model(
            f"{self._base}/equip",
            EquipRequestSchema,
            json={"code": code, "slot": slot.value, "quantity": quantity},
        )

    @_auto_cooldown
    async def unequip(
        self, *, slot: ItemSlot, quantity: int = 1
    ) -> EquipRequestSchema:
        """Unequip an item from a slot."""
        return await self._http.post_model(
            f"{self._base}/unequip",
            EquipRequestSchema,
            json={"slot": slot.value, "quantity": quantity},
        )
