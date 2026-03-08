"""Inventory domain -- item usage and deletion."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.responses import DeleteItemSchema, UseItemSchema
from ._base import CharacterDomain


class InventoryDomain(CharacterDomain):
    """Manage inventory items.

    Accessed via ``character.inventory``::

        await char.inventory.use(code="cooked_chicken", quantity=2)
        await char.inventory.delete(code="old_sword")
    """

    @_auto_cooldown
    async def use(self, *, code: str, quantity: int = 1) -> UseItemSchema:
        """Use a consumable item from inventory."""
        return await self._http.post_model(
            f"{self._base}/use",
            UseItemSchema,
            json={"code": code, "quantity": quantity},
        )

    @_auto_cooldown
    async def delete(self, *, code: str, quantity: int = 1) -> DeleteItemSchema:
        """Permanently delete an item from inventory."""
        return await self._http.post_model(
            f"{self._base}/delete",
            DeleteItemSchema,
            json={"code": code, "quantity": quantity},
        )
