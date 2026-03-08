"""Character controller -- slim SDK entry point.

Delegates domain-specific actions to sub-objects while keeping
combat, movement, and misc actions directly accessible.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Union

from .cooldown import _auto_cooldown
from .domains.bank import BankDomain
from .domains.equipment import EquipmentDomain
from .domains.ge import GrandExchangeDomain
from .domains.inventory import InventoryDomain
from .domains.skills import SkillsDomain
from .domains.tasks import TasksDomain
from .domains.trading import TradingDomain
from .models.character import CharacterSchema
from .models.enums import CharacterSkin
from .models.logs import LogSchema
from .models.pagination import DataPage
from .models.responses import (
    ChangeSkinCharacterDataSchema,
    CharacterFightDataSchema,
    CharacterMovementDataSchema,
    CharacterRestDataSchema,
    CharacterTransitionDataSchema,
    ClaimPendingItemDataSchema,
)

if TYPE_CHECKING:
    from .http import HttpClient


class Character:
    """Controller for a single character.

    Created via ``client.character("name")``.  Actions are organized
    into game-oriented sub-objects::

        char = client.character("MyChar")

        # Direct actions (combat & movement)
        await char.move(x=0, y=1)
        await char.fight()
        await char.rest()

        # Domain sub-objects
        await char.skills.craft(code="iron_sword")
        await char.bank.deposit_gold(quantity=100)
        await char.equipment.equip(code="iron_sword", slot=ItemSlot.WEAPON)
        await char.inventory.use(code="cooked_chicken")
        await char.tasks.new()
        await char.ge.sell(code="iron_ore", quantity=10, price=5)
        await char.trading.npc_buy(code="healing_potion")

    By default, the SDK automatically waits for cooldowns before each
    action so that results are returned immediately.  Override per-call
    with ``wait=False``::

        result = await char.fight(wait=False)  # returns immediately
    """

    def __init__(self, name: str, http: HttpClient, *, auto_wait: Union[bool, list] = True):
        self.name = name
        self._http = http
        self._base = f"/my/{name}/action"
        # Accept either a plain bool (per-character override) or a shared
        # mutable list[bool] coming from the client so that changes to
        # ``client.auto_wait`` propagate instantly to all active instances.
        self._auto_wait_source: Union[bool, list] = (
            auto_wait if isinstance(auto_wait, list) else [auto_wait]
        )
        # Shared cooldown expiry timestamp (monotonic).  Passed to all domains
        # so that any action (fight, gather, etc.) updates the same state.
        self._cooldown_ref: list = [None]

        # -- Domain sub-objects (share the same mutable sources) --
        self.inventory = InventoryDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.bank = BankDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.equipment = EquipmentDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.skills = SkillsDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.tasks = TasksDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.ge = GrandExchangeDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)
        self.trading = TradingDomain(name, http, auto_wait=self._auto_wait_source, cooldown_ref=self._cooldown_ref)

    @property
    def _auto_wait(self) -> bool:
        return self._auto_wait_source[0]

    @_auto_wait.setter
    def _auto_wait(self, value: bool) -> None:
        self._auto_wait_source[0] = value

    @property
    def _cooldown_until(self) -> Optional[float]:
        return self._cooldown_ref[0]

    @_cooldown_until.setter
    def _cooldown_until(self, value: Optional[float]) -> None:
        self._cooldown_ref[0] = value

    def __repr__(self) -> str:
        return f"Character({self.name!r})"

    # ------------------------------------------------------------------ #
    #  Character info (no cooldown)                                       #
    # ------------------------------------------------------------------ #

    async def get(self) -> CharacterSchema:
        """Fetch full character info (GET /characters/{name})."""
        return await self._http.get_model(
            f"/characters/{self.name}", CharacterSchema
        )

    async def get_logs(
        self, *, page: int = 1, size: int = 50
    ) -> DataPage[LogSchema]:
        """Fetch character action history (GET /my/logs/{name})."""
        return await self._http.get_page(
            f"/my/logs/{self.name}",
            LogSchema,
            params={"page": page, "size": size},
        )

    # ------------------------------------------------------------------ #
    #  Movement                                                           #
    # ------------------------------------------------------------------ #

    @_auto_cooldown
    async def move(
        self,
        *,
        x: Optional[int] = None,
        y: Optional[int] = None,
        map_id: Optional[int] = None,
    ) -> CharacterMovementDataSchema:
        """Move the character.

        Provide either ``map_id`` or ``x`` + ``y`` coordinates.
        """
        body: dict = {}
        if map_id is not None:
            body["map_id"] = map_id
        else:
            body["x"] = x
            body["y"] = y
        return await self._http.post_model(
            f"{self._base}/move", CharacterMovementDataSchema, json=body
        )

    @_auto_cooldown
    async def transition(self) -> CharacterTransitionDataSchema:
        """Execute a layer transition (go underground, enter building, etc.)."""
        return await self._http.post_model(
            f"{self._base}/transition", CharacterTransitionDataSchema
        )

    # ------------------------------------------------------------------ #
    #  Combat                                                             #
    # ------------------------------------------------------------------ #

    @_auto_cooldown
    async def fight(
        self, *, participants: Optional[list[str]] = None
    ) -> CharacterFightDataSchema:
        """Fight a monster on the current map tile.

        For bosses, pass up to 2 additional character names in
        ``participants``.
        """
        body: dict = {}
        if participants:
            body["participants"] = participants
        return await self._http.post_model(
            f"{self._base}/fight", CharacterFightDataSchema, json=body or None
        )

    @_auto_cooldown
    async def rest(self) -> CharacterRestDataSchema:
        """Rest to recover HP."""
        return await self._http.post_model(
            f"{self._base}/rest", CharacterRestDataSchema
        )

    # ------------------------------------------------------------------ #
    #  Misc                                                               #
    # ------------------------------------------------------------------ #

    @_auto_cooldown
    async def claim_item(self, id: int) -> ClaimPendingItemDataSchema:
        """Claim a pending item."""
        return await self._http.post_model(
            f"{self._base}/claim_item/{id}", ClaimPendingItemDataSchema
        )

    @_auto_cooldown
    async def change_skin(
        self, *, skin: CharacterSkin
    ) -> ChangeSkinCharacterDataSchema:
        """Change character skin."""
        return await self._http.post_model(
            f"{self._base}/change_skin",
            ChangeSkinCharacterDataSchema,
            json={"skin": skin.value},
        )
