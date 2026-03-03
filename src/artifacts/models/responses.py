from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .bank import BankExtensionSchema, BankSchema
from .character import CharacterSchema
from .combat import CharacterFightSchema
from .common import (
    CooldownSchema,
    DestinationSchema,
    DropSchema,
    SimpleItemSchema,
)
from .enums import CharacterSkin, ItemSlot
from .grand_exchange import GEOrderCreatedSchema, GETransactionSchema
from .maps import MapSchema, TransitionSchema
from .npcs import NpcItemTransactionSchema
from .tasks import TaskSchema, TaskTradeSchema


# -- Movement --

class CharacterMovementDataSchema(BaseModel):
    cooldown: CooldownSchema
    destination: MapSchema
    path: list[list[int]]
    character: CharacterSchema


class CharacterTransitionDataSchema(BaseModel):
    cooldown: CooldownSchema
    destination: MapSchema
    transition: TransitionSchema
    character: CharacterSchema


# -- Combat --

class CharacterFightDataSchema(BaseModel):
    cooldown: CooldownSchema
    fight: CharacterFightSchema
    characters: list[CharacterSchema]


class CharacterRestDataSchema(BaseModel):
    cooldown: CooldownSchema
    hp_restored: int
    character: CharacterSchema


# -- Equipment --

class EquipRequestSchema(BaseModel):
    cooldown: CooldownSchema
    slot: ItemSlot
    item: SimpleItemSchema
    character: CharacterSchema


# -- Skills --

class SkillInfoSchema(BaseModel):
    xp: int
    items: list[DropSchema]


class SkillDataSchema(BaseModel):
    cooldown: CooldownSchema
    details: SkillInfoSchema
    character: CharacterSchema


class RecyclingItemsSchema(BaseModel):
    items: list[DropSchema]


class RecyclingDataSchema(BaseModel):
    cooldown: CooldownSchema
    details: RecyclingItemsSchema
    character: CharacterSchema


# -- Items --

class UseItemSchema(BaseModel):
    cooldown: CooldownSchema
    item: SimpleItemSchema
    character: CharacterSchema


class DeleteItemSchema(BaseModel):
    cooldown: CooldownSchema
    item: SimpleItemSchema
    character: CharacterSchema


# -- Bank --

class BankGoldTransactionSchema(BaseModel):
    cooldown: CooldownSchema
    bank: BankSchema
    character: CharacterSchema


class BankItemTransactionSchema(BaseModel):
    cooldown: CooldownSchema
    items: list[SimpleItemSchema]
    bank: list[SimpleItemSchema]
    character: CharacterSchema


class BankExtensionTransactionSchema(BaseModel):
    cooldown: CooldownSchema
    transaction: BankExtensionSchema
    character: CharacterSchema


# -- NPC --

class NpcMerchantTransactionSchema(BaseModel):
    cooldown: CooldownSchema
    transaction: NpcItemTransactionSchema
    character: CharacterSchema


# -- Grand Exchange --

class GEOrderTransactionSchema(BaseModel):
    cooldown: CooldownSchema
    order: GEOrderCreatedSchema
    character: CharacterSchema


class GETransactionListSchema(BaseModel):
    cooldown: CooldownSchema
    order: GETransactionSchema
    character: CharacterSchema


# -- Tasks --

class TaskDataSchema(BaseModel):
    cooldown: CooldownSchema
    task: TaskSchema
    character: CharacterSchema


class TaskCancelledSchema(BaseModel):
    cooldown: CooldownSchema
    character: CharacterSchema


class RewardDataSchema(BaseModel):
    cooldown: CooldownSchema
    rewards: dict
    character: CharacterSchema


class TaskTradeDataSchema(BaseModel):
    cooldown: CooldownSchema
    trade: TaskTradeSchema
    character: CharacterSchema


# -- Give --

class GiveGoldDataSchema(BaseModel):
    cooldown: CooldownSchema
    quantity: int
    receiver_character: CharacterSchema
    character: CharacterSchema


class GiveItemDataSchema(BaseModel):
    cooldown: CooldownSchema
    items: list[SimpleItemSchema]
    receiver_character: CharacterSchema
    character: CharacterSchema


# -- Misc --

class ClaimPendingItemDataSchema(BaseModel):
    cooldown: CooldownSchema
    item: SimpleItemSchema
    character: CharacterSchema


class ChangeSkinCharacterDataSchema(BaseModel):
    cooldown: CooldownSchema
    skin: CharacterSkin
    character: CharacterSchema
