"""Tasks domain -- task lifecycle management."""

from __future__ import annotations

from ..cooldown import _auto_cooldown
from ..models.responses import (
    RewardDataSchema,
    TaskCancelledSchema,
    TaskDataSchema,
    TaskTradeDataSchema,
)
from ._base import CharacterDomain


class TasksDomain(CharacterDomain):
    """Manage tasks from the Tasks Master.

    Accessed via ``character.tasks``::

        await char.tasks.new()
        await char.tasks.trade(code="iron_ore", quantity=10)
        await char.tasks.complete()
        await char.tasks.exchange()
    """

    @_auto_cooldown
    async def new(self) -> TaskDataSchema:
        """Accept a new task from the Tasks Master."""
        return await self._http.post_model(
            f"{self._base}/task/new", TaskDataSchema
        )

    @_auto_cooldown
    async def complete(self) -> RewardDataSchema:
        """Complete and turn in the current task."""
        return await self._http.post_model(
            f"{self._base}/task/complete", RewardDataSchema
        )

    @_auto_cooldown
    async def exchange(self) -> RewardDataSchema:
        """Exchange 6 task coins for a reward."""
        return await self._http.post_model(
            f"{self._base}/task/exchange", RewardDataSchema
        )

    @_auto_cooldown
    async def trade(self, *, code: str, quantity: int) -> TaskTradeDataSchema:
        """Trade items with the Tasks Master."""
        return await self._http.post_model(
            f"{self._base}/task/trade",
            TaskTradeDataSchema,
            json={"code": code, "quantity": quantity},
        )

    @_auto_cooldown
    async def cancel(self) -> TaskCancelledSchema:
        """Cancel the current task (costs 1 task coin)."""
        return await self._http.post_model(
            f"{self._base}/task/cancel", TaskCancelledSchema
        )
