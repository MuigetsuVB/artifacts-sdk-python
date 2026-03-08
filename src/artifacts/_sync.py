"""Internal sync-wrapper utilities for the Artifacts SDK.

Provides a way to run async coroutines synchronously using a
dedicated background event loop in a daemon thread.  This approach
is compatible with Jupyter notebooks, IPython, and any environment
that already has a running event loop (where ``asyncio.run()``
would fail).
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any, Coroutine, TypeVar

T = TypeVar("T")

_loop: asyncio.AbstractEventLoop | None = None
_thread: threading.Thread | None = None
_lock = threading.Lock()


def _get_loop() -> asyncio.AbstractEventLoop:
    """Return (and lazily create) a dedicated background event loop."""
    global _loop, _thread
    with _lock:
        if _loop is None or _loop.is_closed():
            _loop = asyncio.new_event_loop()
            _thread = threading.Thread(target=_loop.run_forever, daemon=True)
            _thread.start()
    return _loop


def run_sync(coro: Coroutine[Any, Any, T]) -> T:
    """Run an async coroutine synchronously and return the result.

    Uses a background thread running an event loop so that it works
    even inside environments with a running loop (Jupyter, IPython).
    """
    loop = _get_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()
