from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import ActionType, ConditionOperator


class CooldownSchema(BaseModel):
    total_seconds: int
    remaining_seconds: int
    started_at: str
    expiration: str
    reason: ActionType


class SimpleItemSchema(BaseModel):
    code: str
    quantity: int


class DropSchema(BaseModel):
    code: str
    quantity: int


class InventorySlot(BaseModel):
    slot: int
    code: str
    quantity: int


class DestinationSchema(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None
    map_id: Optional[int] = None


class StorageEffectSchema(BaseModel):
    code: str
    value: int


class SimpleEffectSchema(BaseModel):
    code: str
    value: int
    description: Optional[str] = None


class ConditionSchema(BaseModel):
    code: str
    operator: ConditionOperator
    value: Optional[int] = None


class RewardItemSchema(BaseModel):
    code: str
    quantity: int


class RewardsSchema(BaseModel):
    items: list[SimpleItemSchema]
    gold: int


class GoldSchema(BaseModel):
    quantity: int
