"""Main client entry point for the Artifacts MMO SDK."""

from __future__ import annotations

from typing import Optional

from .character import Character
from .http import HttpClient, RetryConfig
from .api.accounts import AccountsAPI
from .api.achievements import AchievementsAPI
from .api.badges import BadgesAPI
from .api.characters import CharactersAPI
from .api.effects import EffectsAPI
from .api.events import EventsAPI
from .api.grand_exchange import GrandExchangeAPI
from .api.items import ItemsAPI
from .api.leaderboard import LeaderboardAPI
from .api.maps import MapsAPI
from .api.monsters import MonstersAPI
from .api.my_account import MyAccountAPI
from .api.npcs import NPCsAPI
from .api.resources import ResourcesAPI
from .api.sandbox import SandboxAPI
from .api.server import ServerAPI
from .api.simulation import SimulationAPI
from .api.tasks import TasksAPI
from .api.token import TokenAPI


class AsyncArtifactsClient:
    """Async SDK client for the Artifacts MMO API.

    Use as an async context manager::

        async with AsyncArtifactsClient(token="your_token") as client:
            char = client.character("MyChar")
            await char.move(x=0, y=1)    # auto-waits cooldown
            await char.fight()            # auto-waits cooldown

    Parameters
    ----------
    token:
        JWT token for authentication.  Generate one via
        ``client.token.generate(username, password)`` or pass an
        existing token.
    base_url:
        API base URL.  Defaults to the production server.
    auto_wait:
        If ``True`` (default), every action automatically sleeps
        until its cooldown expires.  Disable globally here or
        per-character/per-call.
    retry:
        Custom retry configuration.  Defaults to 3 retries with
        exponential backoff.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        base_url: str = "https://api.artifactsmmo.com",
        auto_wait: bool = True,
        retry: Optional[RetryConfig] = None,
    ):
        self._http = HttpClient(base_url=base_url, token=token, retry=retry)
        # Shared mutable reference so that ``client.auto_wait = False``
        # propagates instantly to every Character/Domain created from this client.
        self._auto_wait_ref: list = [auto_wait]

        # -- Sub-accessors (game data & account) --
        self.server = ServerAPI(self._http)
        self.token = TokenAPI(self._http)
        self.accounts = AccountsAPI(self._http)
        self.my_account = MyAccountAPI(self._http)
        self.characters = CharactersAPI(self._http)
        self.achievements = AchievementsAPI(self._http)
        self.badges = BadgesAPI(self._http)
        self.effects = EffectsAPI(self._http)
        self.events = EventsAPI(self._http)
        self.grand_exchange = GrandExchangeAPI(self._http)
        self.items = ItemsAPI(self._http)
        self.leaderboard = LeaderboardAPI(self._http)
        self.maps = MapsAPI(self._http)
        self.monsters = MonstersAPI(self._http)
        self.npcs = NPCsAPI(self._http)
        self.resources = ResourcesAPI(self._http)
        self.tasks = TasksAPI(self._http)
        self.simulation = SimulationAPI(self._http)
        self.sandbox = SandboxAPI(self._http)

    # -- Global auto_wait toggle --

    @property
    def auto_wait(self) -> bool:
        """Whether actions automatically sleep until their cooldown expires.

        Setting this on the client affects **all** characters that were
        created without an explicit per-character override::

            client.auto_wait = False   # disable globally
            client.auto_wait = True    # re-enable globally
        """
        return self._auto_wait_ref[0]

    @auto_wait.setter
    def auto_wait(self, value: bool) -> None:
        self._auto_wait_ref[0] = value

    # -- Character factory --

    def character(self, name: str, *, auto_wait: Optional[bool] = None) -> Character:
        """Return a :class:`Character` controller for *name*.

        Parameters
        ----------
        auto_wait:
            Override the client-level ``auto_wait`` setting for this
            character.  If ``None`` (default), the character shares the
            client reference and will reflect any future changes to
            ``client.auto_wait`` automatically.
        """
        # Per-character override: pass a plain bool (isolated copy).
        # No override: pass the shared mutable list so the character
        # tracks the client-level setting dynamically.
        source = [auto_wait] if auto_wait is not None else self._auto_wait_ref
        return Character(name=name, http=self._http, auto_wait=source)

    # -- Context manager --

    async def start(self) -> None:
        """Start the HTTP session (called automatically by ``__aenter__``)."""
        await self._http.start()

    async def close(self) -> None:
        """Close the HTTP session (called automatically by ``__aexit__``)."""
        await self._http.close()

    async def __aenter__(self) -> AsyncArtifactsClient:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
