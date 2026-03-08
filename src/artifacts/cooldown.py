"""Cooldown helpers for the Artifacts SDK."""

from __future__ import annotations

import asyncio
import functools
import logging
import time
from typing import Any, Callable, TypeVar

from .models.common import CooldownSchema

logger = logging.getLogger("artifacts.cooldown")

F = TypeVar("F", bound=Callable[..., Any])


async def wait_for_cooldown(cooldown: CooldownSchema) -> None:
    """Sleep for the remaining cooldown duration.

    Call this explicitly after an action if you want to wait::

        result = await char.fight()
        await wait_for_cooldown(result.cooldown)

    .. note::

       When ``auto_wait`` is enabled (the default), the SDK waits
       automatically before the *next* action.  You only need to call
       this manually when ``auto_wait`` is disabled.
    """
    if cooldown.remaining_seconds > 0:
        await asyncio.sleep(cooldown.remaining_seconds)


def cooldown_seconds(cooldown: CooldownSchema) -> int:
    """Return the remaining seconds from a cooldown."""
    return cooldown.remaining_seconds


def _auto_cooldown(method: F) -> F:
    """Decorator: automatically waits for the previous cooldown before an action.

    Reads ``self._auto_wait`` to decide.  Can be overridden per-call
    via a ``wait`` keyword argument::

        await char.fight()              # auto-waits (default)
        await char.fight(wait=False)    # returns immediately

    The wait happens **before** the action so that the result is returned
    immediately after execution, without blocking on the cooldown.
    """

    @functools.wraps(method)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        # Extract per-call override
        wait = kwargs.pop("wait", None)
        should_wait = wait if wait is not None else self._auto_wait

        # BEFORE: wait for the cooldown from the previous action
        if should_wait:
            until = self._cooldown_until
            if until is not None:
                remaining = until - time.monotonic()
                if remaining > 0:
                    logger.debug(
                        "Auto-waiting %.1fs cooldown before %s.%s",
                        remaining,
                        type(self).__name__,
                        method.__name__,
                    )
                    await asyncio.sleep(remaining)
            self._cooldown_until = None

        result = await method(self, *args, **kwargs)

        # AFTER: store expiry, return immediately
        if should_wait and hasattr(result, "cooldown"):
            cd = result.cooldown
            if cd.remaining_seconds > 0:
                self._cooldown_until = time.monotonic() + cd.remaining_seconds

        return result

    return wrapper  # type: ignore[return-value]
