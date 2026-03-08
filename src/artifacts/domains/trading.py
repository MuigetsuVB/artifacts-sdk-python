"""Trading domain -- NPC merchants and player-to-player transfers."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.common import SimpleItemSchema
from ..models.responses import (
    GiveGoldDataSchema,
    GiveItemDataSchema,
    NpcMerchantTransactionSchema,
)
from ._base import CharacterDomain


class TradingDomain(CharacterDomain):
    """Manage NPC trading and player-to-player transfers.

    Accessed via ``character.trading``::

        await char.trading.npc_buy(code="healing_potion", quantity=5)
        await char.trading.npc_sell(code="iron_ore", quantity=10)
        await char.trading.give_gold(quantity=100, character="Friend")
    """

    @_auto_cooldown
    async def npc_buy(
        self, *, code: str, quantity: int = 1
    ) -> NpcMerchantTransactionSchema:
        """Buy from an NPC merchant."""
        return await self._http.post_model(
            f"{self._base}/npc/buy",
            NpcMerchantTransactionSchema,
            json={"code": code, "quantity": quantity},
        )

    @_auto_cooldown
    async def npc_sell(
        self, *, code: str, quantity: int = 1
    ) -> NpcMerchantTransactionSchema:
        """Sell to an NPC merchant."""
        return await self._http.post_model(
            f"{self._base}/npc/sell",
            NpcMerchantTransactionSchema,
            json={"code": code, "quantity": quantity},
        )

    @_auto_cooldown
    async def give_gold(
        self, *, quantity: int, character: str
    ) -> GiveGoldDataSchema:
        """Give gold to another character."""
        return await self._http.post_model(
            f"{self._base}/give/gold",
            GiveGoldDataSchema,
            json={"quantity": quantity, "character": character},
        )

    @_auto_cooldown
    async def give_items(
        self, *, items: list[SimpleItemSchema], character: str
    ) -> GiveItemDataSchema:
        """Give items to another character."""
        return await self._http.post_model(
            f"{self._base}/give/item",
            GiveItemDataSchema,
            json={
                "items": [i.model_dump() for i in items],
                "character": character,
            },
        )
