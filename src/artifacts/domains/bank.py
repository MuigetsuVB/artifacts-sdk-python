"""Bank domain -- gold and item deposits/withdrawals."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.common import SimpleItemSchema
from ..models.responses import (
    BankExtensionTransactionSchema,
    BankGoldTransactionSchema,
    BankItemTransactionSchema,
)
from ._base import CharacterDomain


class BankDomain(CharacterDomain):
    """Manage bank operations.

    Accessed via ``character.bank``::

        await char.bank.deposit_gold(quantity=500)
        await char.bank.withdraw_items(items=[SimpleItemSchema(code="iron_ore", quantity=10)])
        await char.bank.buy_expansion()
    """

    @_auto_cooldown
    async def deposit_gold(self, *, quantity: int) -> BankGoldTransactionSchema:
        """Deposit gold into the bank."""
        return await self._http.post_model(
            f"{self._base}/bank/deposit/gold",
            BankGoldTransactionSchema,
            json={"quantity": quantity},
        )

    @_auto_cooldown
    async def withdraw_gold(self, *, quantity: int) -> BankGoldTransactionSchema:
        """Withdraw gold from the bank."""
        return await self._http.post_model(
            f"{self._base}/bank/withdraw/gold",
            BankGoldTransactionSchema,
            json={"quantity": quantity},
        )

    @_auto_cooldown
    async def deposit_items(
        self, items: list[SimpleItemSchema]
    ) -> BankItemTransactionSchema:
        """Deposit items into the bank."""
        return await self._http.post_model(
            f"{self._base}/bank/deposit/item",
            BankItemTransactionSchema,
            json=[i.model_dump() for i in items],
        )

    @_auto_cooldown
    async def withdraw_items(
        self, items: list[SimpleItemSchema]
    ) -> BankItemTransactionSchema:
        """Withdraw items from the bank."""
        return await self._http.post_model(
            f"{self._base}/bank/withdraw/item",
            BankItemTransactionSchema,
            json=[i.model_dump() for i in items],
        )

    @_auto_cooldown
    async def buy_expansion(self) -> BankExtensionTransactionSchema:
        """Purchase a 20-slot bank expansion."""
        return await self._http.post_model(
            f"{self._base}/bank/buy_expansion",
            BankExtensionTransactionSchema,
        )
