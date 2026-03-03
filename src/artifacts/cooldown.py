"""Cooldown helpers for the Artifacts wrapper."""

from __future__ import annotations

import asyncio

from .models.common import CooldownSchema


async def wait_for_cooldown(cooldown: CooldownSchema) -> None:
    """Sleep for the remaining cooldown duration.

    Call this explicitly after an action if you want to wait::

        result = await char.fight()
        await wait_for_cooldown(result.cooldown)

    This function is never called automatically by the wrapper.
    """
    if cooldown.remaining_seconds > 0:
        await asyncio.sleep(cooldown.remaining_seconds)


def cooldown_seconds(cooldown: CooldownSchema) -> int:
    """Return the remaining seconds from a cooldown."""
    return cooldown.remaining_seconds
