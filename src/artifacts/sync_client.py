"""Synchronous SDK client -- no async/await required.

Wraps the async :class:`AsyncArtifactsClient` so beginners can write
simple, blocking code::

    from artifacts import ArtifactsClient

    with ArtifactsClient(token="your_token") as client:
        char = client.character("MyChar")
        char.move(x=0, y=1)
        result = char.fight()
        print(result.fight.result)
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from ._sync import run_sync
from .domains._base import CharacterDomain


class _SyncProxy:
    """Generic proxy that turns async method calls into synchronous ones."""

    def __init__(self, async_obj: Any):
        object.__setattr__(self, "_async_obj", async_obj)

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._async_obj, name)

        # Sub-domain objects get wrapped too
        if isinstance(attr, CharacterDomain):
            return _SyncProxy(attr)

        # Async methods become blocking calls
        if asyncio.iscoroutinefunction(attr):
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return run_sync(attr(*args, **kwargs))
            sync_wrapper.__name__ = name
            sync_wrapper.__doc__ = attr.__doc__
            return sync_wrapper

        return attr

    def __repr__(self) -> str:
        return f"Sync({self._async_obj!r})"


class SyncCharacter(_SyncProxy):
    """Synchronous character controller.

    All methods block until complete (including cooldown wait when
    ``auto_wait`` is enabled).

    Created via ``client.character("name")``::

        char = client.character("MyChar")
        char.fight()   # blocks, returns result
    """

    @property
    def name(self) -> str:
        return self._async_obj.name

    @property
    def inventory(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.inventory)

    @property
    def bank(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.bank)

    @property
    def equipment(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.equipment)

    @property
    def skills(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.skills)

    @property
    def tasks(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.tasks)

    @property
    def ge(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.ge)

    @property
    def trading(self) -> _SyncProxy:
        return _SyncProxy(self._async_obj.trading)


class ArtifactsClient:
    """Synchronous SDK client for the Artifacts MMO API.

    No ``async``/``await`` needed -- every call blocks until complete::

        from artifacts import ArtifactsClient

        with ArtifactsClient(token="your_token") as client:
            char = client.character("MyChar")
            info = char.get()
            print(f"{info.name} lv{info.level}")

            char.move(x=0, y=1)          # blocks, auto-waits cooldown
            result = char.fight()         # blocks, auto-waits cooldown
            char.skills.craft(code="iron_sword")
            char.bank.deposit_gold(quantity=100)

    Parameters
    ----------
    token:
        JWT token for authentication.
    base_url:
        API base URL.  Defaults to the production server.
    auto_wait:
        If ``True`` (default), every action automatically sleeps
        until its cooldown expires.
    retry:
        Custom retry configuration.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        base_url: str = "https://api.artifactsmmo.com",
        auto_wait: bool = True,
        retry: Any = None,
    ):
        from .client import AsyncArtifactsClient

        self._async_client = AsyncArtifactsClient(
            token=token,
            base_url=base_url,
            auto_wait=auto_wait,
            retry=retry,
        )
        run_sync(self._async_client.start())

    # -- Character factory --

    def character(
        self, name: str, *, auto_wait: Optional[bool] = None
    ) -> SyncCharacter:
        """Return a synchronous :class:`SyncCharacter` controller for *name*."""
        async_char = self._async_client.character(name, auto_wait=auto_wait)
        return SyncCharacter(async_char)

    # -- Global auto_wait toggle --

    @property
    def auto_wait(self) -> bool:
        """Whether actions automatically sleep until their cooldown expires.

        Setting this on the client affects **all** characters that were
        created without an explicit per-character override::

            client.auto_wait = False   # disable globally
            client.auto_wait = True    # re-enable globally
        """
        return self._async_client.auto_wait

    @auto_wait.setter
    def auto_wait(self, value: bool) -> None:
        self._async_client.auto_wait = value

    # -- Data API sub-accessors (sync proxies) --

    @property
    def server(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.server)

    @property
    def token(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.token)

    @property
    def accounts(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.accounts)

    @property
    def my_account(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.my_account)

    @property
    def characters(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.characters)

    @property
    def achievements(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.achievements)

    @property
    def badges(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.badges)

    @property
    def effects(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.effects)

    @property
    def events(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.events)

    @property
    def grand_exchange(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.grand_exchange)

    @property
    def items(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.items)

    @property
    def leaderboard(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.leaderboard)

    @property
    def maps(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.maps)

    @property
    def monsters(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.monsters)

    @property
    def npcs(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.npcs)

    @property
    def resources(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.resources)

    @property
    def tasks(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.tasks)

    @property
    def simulation(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.simulation)

    @property
    def sandbox(self) -> _SyncProxy:
        return _SyncProxy(self._async_client.sandbox)

    # -- Lifecycle --

    def close(self) -> None:
        """Close the HTTP session."""
        run_sync(self._async_client.close())

    def __enter__(self) -> ArtifactsClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass
