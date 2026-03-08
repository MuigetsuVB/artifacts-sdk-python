"""Grand Exchange domain -- Grand Exchange operations."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.responses import GEOrderTransactionSchema, GETransactionListSchema
from ._base import CharacterDomain


class GrandExchangeDomain(CharacterDomain):
    """Manage Grand Exchange operations.

    Accessed via ``character.ge``::

        await char.ge.sell(code="iron_ore", quantity=10, price=5)
        await char.ge.buy(id="order-123", quantity=5)
        await char.ge.cancel(id="order-123")
    """

    @_auto_cooldown
    async def buy(self, *, id: str, quantity: int) -> GETransactionListSchema:
        """Buy items from an existing sell order."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/buy",
            GETransactionListSchema,
            json={"id": id, "quantity": quantity},
        )

    @_auto_cooldown
    async def sell(
        self, *, code: str, quantity: int, price: int
    ) -> GEOrderTransactionSchema:
        """Create a sell order on the Grand Exchange."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/create-sell-order",
            GEOrderTransactionSchema,
            json={"code": code, "quantity": quantity, "price": price},
        )

    @_auto_cooldown
    async def create_buy_order(
        self, *, code: str, quantity: int, price: int
    ) -> GEOrderTransactionSchema:
        """Create a buy order on the Grand Exchange."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/create-buy-order",
            GEOrderTransactionSchema,
            json={"code": code, "quantity": quantity, "price": price},
        )

    @_auto_cooldown
    async def fill(self, *, id: str, quantity: int) -> GETransactionListSchema:
        """Fill an existing buy order."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/fill",
            GETransactionListSchema,
            json={"id": id, "quantity": quantity},
        )

    @_auto_cooldown
    async def cancel(self, *, id: str) -> GEOrderTransactionSchema:
        """Cancel an existing order."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/cancel",
            GEOrderTransactionSchema,
            json={"id": id},
        )
