"""Main client entry point for the Artifacts MMO API wrapper."""

from __future__ import annotations

from typing import Optional

from .character import Character
from .http import HttpClient
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


class ArtifactsClient:
    """Async client for the Artifacts MMO API.

    Use as an async context manager::

        async with ArtifactsClient(token="your_token") as client:
            char = client.character("MyChar")
            result = await char.fight()

    Parameters
    ----------
    token:
        JWT token for authentication.  Generate one via
        ``client.token.generate(username, password)`` or pass an
        existing token.
    base_url:
        API base URL.  Defaults to the production server.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        base_url: str = "https://api.artifactsmmo.com",
    ):
        self._http = HttpClient(base_url=base_url, token=token)

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

    # -- Character factory --

    def character(self, name: str) -> Character:
        """Return a :class:`Character` controller for *name*."""
        return Character(name=name, http=self._http)

    # -- Context manager --

    async def start(self) -> None:
        """Start the HTTP session (called automatically by ``__aenter__``)."""
        await self._http.start()

    async def close(self) -> None:
        """Close the HTTP session (called automatically by ``__aexit__``)."""
        await self._http.close()

    async def __aenter__(self) -> ArtifactsClient:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
