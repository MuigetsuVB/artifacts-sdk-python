"""Character controller -- all /my/{name}/action/* endpoints."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .models.character import CharacterSchema
from .models.common import SimpleItemSchema
from .models.enums import CharacterSkin, ItemSlot
from .models.logs import LogSchema
from .models.pagination import DataPage
from .models.responses import (
    BankExtensionTransactionSchema,
    BankGoldTransactionSchema,
    BankItemTransactionSchema,
    ChangeSkinCharacterDataSchema,
    CharacterFightDataSchema,
    CharacterMovementDataSchema,
    CharacterRestDataSchema,
    CharacterTransitionDataSchema,
    ClaimPendingItemDataSchema,
    DeleteItemSchema,
    EquipRequestSchema,
    GEOrderTransactionSchema,
    GETransactionListSchema,
    GiveGoldDataSchema,
    GiveItemDataSchema,
    NpcMerchantTransactionSchema,
    RecyclingDataSchema,
    RewardDataSchema,
    SkillDataSchema,
    TaskCancelledSchema,
    TaskDataSchema,
    TaskTradeDataSchema,
    UseItemSchema,
)

if TYPE_CHECKING:
    from .http import HttpClient


class Character:
    """Controller for a single character.

    Created via ``client.character("name")``.  Every action method
    corresponds to a ``POST /my/{name}/action/*`` endpoint.

    Example::

        char = client.character("MyChar")
        info = await char.get()
        result = await char.fight()
        await wait_for_cooldown(result.cooldown)
    """

    def __init__(self, name: str, http: HttpClient):
        self.name = name
        self._http = http
        self._base = f"/my/{name}/action"

    def __repr__(self) -> str:
        return f"Character({self.name!r})"

    # ------------------------------------------------------------------ #
    #  Character info                                                     #
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

    async def move(
        self,
        *,
        x: Optional[int] = None,
        y: Optional[int] = None,
        map_id: Optional[int] = None,
    ) -> CharacterMovementDataSchema:
        """Move the character (POST /my/{name}/action/move).

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

    async def transition(self) -> CharacterTransitionDataSchema:
        """Execute a layer transition (POST /my/{name}/action/transition)."""
        return await self._http.post_model(
            f"{self._base}/transition", CharacterTransitionDataSchema
        )

    # ------------------------------------------------------------------ #
    #  Combat                                                             #
    # ------------------------------------------------------------------ #

    async def fight(
        self, *, participants: Optional[list[str]] = None
    ) -> CharacterFightDataSchema:
        """Fight a monster on the map (POST /my/{name}/action/fight).

        For bosses, pass up to 2 additional character names in
        ``participants``.
        """
        body: dict = {}
        if participants:
            body["participants"] = participants
        return await self._http.post_model(
            f"{self._base}/fight", CharacterFightDataSchema, json=body or None
        )

    async def rest(self) -> CharacterRestDataSchema:
        """Rest to recover HP (POST /my/{name}/action/rest)."""
        return await self._http.post_model(
            f"{self._base}/rest", CharacterRestDataSchema
        )

    # ------------------------------------------------------------------ #
    #  Equipment                                                          #
    # ------------------------------------------------------------------ #

    async def equip(
        self, *, code: str, slot: ItemSlot, quantity: int = 1
    ) -> EquipRequestSchema:
        """Equip an item (POST /my/{name}/action/equip)."""
        return await self._http.post_model(
            f"{self._base}/equip",
            EquipRequestSchema,
            json={"code": code, "slot": slot.value, "quantity": quantity},
        )

    async def unequip(
        self, *, slot: ItemSlot, quantity: int = 1
    ) -> EquipRequestSchema:
        """Unequip an item (POST /my/{name}/action/unequip)."""
        return await self._http.post_model(
            f"{self._base}/unequip",
            EquipRequestSchema,
            json={"slot": slot.value, "quantity": quantity},
        )

    # ------------------------------------------------------------------ #
    #  Skills                                                             #
    # ------------------------------------------------------------------ #

    async def gathering(self) -> SkillDataSchema:
        """Gather a resource on the map (POST /my/{name}/action/gathering)."""
        return await self._http.post_model(
            f"{self._base}/gathering", SkillDataSchema
        )

    async def crafting(
        self, *, code: str, quantity: int = 1
    ) -> SkillDataSchema:
        """Craft an item (POST /my/{name}/action/crafting)."""
        return await self._http.post_model(
            f"{self._base}/crafting",
            SkillDataSchema,
            json={"code": code, "quantity": quantity},
        )

    async def recycling(
        self, *, code: str, quantity: int = 1
    ) -> RecyclingDataSchema:
        """Recycle an item (POST /my/{name}/action/recycling)."""
        return await self._http.post_model(
            f"{self._base}/recycling",
            RecyclingDataSchema,
            json={"code": code, "quantity": quantity},
        )

    # ------------------------------------------------------------------ #
    #  Items                                                              #
    # ------------------------------------------------------------------ #

    async def use(
        self, *, code: str, quantity: int = 1
    ) -> UseItemSchema:
        """Use a consumable (POST /my/{name}/action/use)."""
        return await self._http.post_model(
            f"{self._base}/use",
            UseItemSchema,
            json={"code": code, "quantity": quantity},
        )

    async def delete_item(
        self, *, code: str, quantity: int = 1
    ) -> DeleteItemSchema:
        """Delete an item from inventory (POST /my/{name}/action/delete)."""
        return await self._http.post_model(
            f"{self._base}/delete",
            DeleteItemSchema,
            json={"code": code, "quantity": quantity},
        )

    # ------------------------------------------------------------------ #
    #  Bank                                                               #
    # ------------------------------------------------------------------ #

    async def bank_deposit_gold(
        self, *, quantity: int
    ) -> BankGoldTransactionSchema:
        """Deposit gold (POST /my/{name}/action/bank/deposit/gold)."""
        return await self._http.post_model(
            f"{self._base}/bank/deposit/gold",
            BankGoldTransactionSchema,
            json={"quantity": quantity},
        )

    async def bank_withdraw_gold(
        self, *, quantity: int
    ) -> BankGoldTransactionSchema:
        """Withdraw gold (POST /my/{name}/action/bank/withdraw/gold)."""
        return await self._http.post_model(
            f"{self._base}/bank/withdraw/gold",
            BankGoldTransactionSchema,
            json={"quantity": quantity},
        )

    async def bank_deposit_items(
        self, items: list[SimpleItemSchema]
    ) -> BankItemTransactionSchema:
        """Deposit items (POST /my/{name}/action/bank/deposit/item)."""
        return await self._http.post_model(
            f"{self._base}/bank/deposit/item",
            BankItemTransactionSchema,
            json=[i.model_dump() for i in items],
        )

    async def bank_withdraw_items(
        self, items: list[SimpleItemSchema]
    ) -> BankItemTransactionSchema:
        """Withdraw items (POST /my/{name}/action/bank/withdraw/item)."""
        return await self._http.post_model(
            f"{self._base}/bank/withdraw/item",
            BankItemTransactionSchema,
            json=[i.model_dump() for i in items],
        )

    async def bank_buy_expansion(self) -> BankExtensionTransactionSchema:
        """Buy a 20-slot bank expansion (POST /my/{name}/action/bank/buy_expansion)."""
        return await self._http.post_model(
            f"{self._base}/bank/buy_expansion",
            BankExtensionTransactionSchema,
        )

    # ------------------------------------------------------------------ #
    #  NPC                                                                #
    # ------------------------------------------------------------------ #

    async def npc_buy(
        self, *, code: str, quantity: int = 1
    ) -> NpcMerchantTransactionSchema:
        """Buy from an NPC (POST /my/{name}/action/npc/buy)."""
        return await self._http.post_model(
            f"{self._base}/npc/buy",
            NpcMerchantTransactionSchema,
            json={"code": code, "quantity": quantity},
        )

    async def npc_sell(
        self, *, code: str, quantity: int = 1
    ) -> NpcMerchantTransactionSchema:
        """Sell to an NPC (POST /my/{name}/action/npc/sell)."""
        return await self._http.post_model(
            f"{self._base}/npc/sell",
            NpcMerchantTransactionSchema,
            json={"code": code, "quantity": quantity},
        )

    # ------------------------------------------------------------------ #
    #  Grand Exchange                                                     #
    # ------------------------------------------------------------------ #

    async def ge_buy(
        self, *, id: str, quantity: int
    ) -> GETransactionListSchema:
        """Buy from a sell order (POST /my/{name}/action/grandexchange/buy)."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/buy",
            GETransactionListSchema,
            json={"id": id, "quantity": quantity},
        )

    async def ge_create_sell_order(
        self, *, code: str, quantity: int, price: int
    ) -> GEOrderTransactionSchema:
        """Create a sell order (POST /my/{name}/action/grandexchange/create-sell-order)."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/create-sell-order",
            GEOrderTransactionSchema,
            json={"code": code, "quantity": quantity, "price": price},
        )

    async def ge_create_buy_order(
        self, *, code: str, quantity: int, price: int
    ) -> GEOrderTransactionSchema:
        """Create a buy order (POST /my/{name}/action/grandexchange/create-buy-order)."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/create-buy-order",
            GEOrderTransactionSchema,
            json={"code": code, "quantity": quantity, "price": price},
        )

    async def ge_cancel_order(self, *, id: str) -> GEOrderTransactionSchema:
        """Cancel a GE order (POST /my/{name}/action/grandexchange/cancel)."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/cancel",
            GEOrderTransactionSchema,
            json={"id": id},
        )

    async def ge_fill(
        self, *, id: str, quantity: int
    ) -> GETransactionListSchema:
        """Fill a buy order (POST /my/{name}/action/grandexchange/fill)."""
        return await self._http.post_model(
            f"{self._base}/grandexchange/fill",
            GETransactionListSchema,
            json={"id": id, "quantity": quantity},
        )

    # ------------------------------------------------------------------ #
    #  Tasks                                                              #
    # ------------------------------------------------------------------ #

    async def task_new(self) -> TaskDataSchema:
        """Accept a new task (POST /my/{name}/action/task/new)."""
        return await self._http.post_model(
            f"{self._base}/task/new", TaskDataSchema
        )

    async def task_complete(self) -> RewardDataSchema:
        """Complete current task (POST /my/{name}/action/task/complete)."""
        return await self._http.post_model(
            f"{self._base}/task/complete", RewardDataSchema
        )

    async def task_exchange(self) -> RewardDataSchema:
        """Exchange 6 task coins (POST /my/{name}/action/task/exchange)."""
        return await self._http.post_model(
            f"{self._base}/task/exchange", RewardDataSchema
        )

    async def task_trade(
        self, *, code: str, quantity: int
    ) -> TaskTradeDataSchema:
        """Trade items with Tasks Master (POST /my/{name}/action/task/trade)."""
        return await self._http.post_model(
            f"{self._base}/task/trade",
            TaskTradeDataSchema,
            json={"code": code, "quantity": quantity},
        )

    async def task_cancel(self) -> TaskCancelledSchema:
        """Cancel current task for 1 coin (POST /my/{name}/action/task/cancel)."""
        return await self._http.post_model(
            f"{self._base}/task/cancel", TaskCancelledSchema
        )

    # ------------------------------------------------------------------ #
    #  Give                                                               #
    # ------------------------------------------------------------------ #

    async def give_gold(
        self, *, quantity: int, character: str
    ) -> GiveGoldDataSchema:
        """Give gold to another character (POST /my/{name}/action/give/gold)."""
        return await self._http.post_model(
            f"{self._base}/give/gold",
            GiveGoldDataSchema,
            json={"quantity": quantity, "character": character},
        )

    async def give_items(
        self, *, items: list[SimpleItemSchema], character: str
    ) -> GiveItemDataSchema:
        """Give items to another character (POST /my/{name}/action/give/item)."""
        return await self._http.post_model(
            f"{self._base}/give/item",
            GiveItemDataSchema,
            json={
                "items": [i.model_dump() for i in items],
                "character": character,
            },
        )

    # ------------------------------------------------------------------ #
    #  Misc                                                               #
    # ------------------------------------------------------------------ #

    async def claim_item(self, id: int) -> ClaimPendingItemDataSchema:
        """Claim a pending item (POST /my/{name}/action/claim_item/{id})."""
        return await self._http.post_model(
            f"{self._base}/claim_item/{id}", ClaimPendingItemDataSchema
        )

    async def change_skin(
        self, *, skin: CharacterSkin
    ) -> ChangeSkinCharacterDataSchema:
        """Change character skin (POST /my/{name}/action/change_skin)."""
        return await self._http.post_model(
            f"{self._base}/change_skin",
            ChangeSkinCharacterDataSchema,
            json={"skin": skin.value},
        )
