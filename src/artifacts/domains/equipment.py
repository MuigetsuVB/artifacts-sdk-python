"""Equipment domain -- equip and unequip items."""

from __future__ import annotations

from enum import Enum
from typing import Any

from ..cooldown import _auto_cooldown
from ..models.enums import ItemSlot
from ..models.responses import EquipmentTransactionSchema
from ._base import CharacterDomain


def _dump_item(item: Any) -> dict:
    if hasattr(item, "model_dump"):
        return item.model_dump(mode="json", exclude_none=True)
    if hasattr(item, "dict"):
        data = item.dict(exclude_none=True)
    else:
        data = dict(item)
    return {
        key: value.value if isinstance(value, Enum) else value
        for key, value in data.items()
    }


class EquipmentDomain(CharacterDomain):
    """Manage character equipment.

    Accessed via ``character.equipment``::

        await char.equipment.equip(code="iron_sword", slot=ItemSlot.WEAPON)
        await char.equipment.unequip(slot=ItemSlot.HELMET)
    """

    @_auto_cooldown
    async def equip(
        self, *, code: str, slot: ItemSlot, quantity: int = 1
    ) -> EquipmentTransactionSchema:
        """Equip an item into a slot."""
        return await self._equip_items(
            [{"code": code, "slot": slot.value, "quantity": quantity}]
        )

    @_auto_cooldown
    async def equip_items(self, items: list[Any]) -> EquipmentTransactionSchema:
        """Equip one or more items into slots."""
        return await self._equip_items(items)

    async def _equip_items(self, items: list[Any]) -> EquipmentTransactionSchema:
        return await self._http.post_model(
            f"{self._base}/equip",
            EquipmentTransactionSchema,
            json=[_dump_item(item) for item in items],
        )

    @_auto_cooldown
    async def unequip(
        self, *, slot: ItemSlot, quantity: int = 1
    ) -> EquipmentTransactionSchema:
        """Unequip an item from a slot."""
        return await self._unequip_items(
            [{"slot": slot.value, "quantity": quantity}]
        )

    @_auto_cooldown
    async def unequip_items(self, items: list[Any]) -> EquipmentTransactionSchema:
        """Unequip one or more items from slots."""
        return await self._unequip_items(items)

    async def _unequip_items(self, items: list[Any]) -> EquipmentTransactionSchema:
        return await self._http.post_model(
            f"{self._base}/unequip",
            EquipmentTransactionSchema,
            json=[_dump_item(item) for item in items],
        )
