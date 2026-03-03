from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import ConditionSchema, SimpleEffectSchema, SimpleItemSchema
from .enums import CraftSkill, ItemType


class CraftSchema(BaseModel):
    skill: Optional[CraftSkill] = None
    level: Optional[int] = None
    items: list[SimpleItemSchema]
    quantity: int


class ItemSchema(BaseModel):
    name: str
    code: str
    level: int
    type: ItemType
    subtype: Optional[str] = None
    description: Optional[str] = None
    tradeable: bool
    conditions: list[ConditionSchema]
    effects: list[SimpleEffectSchema]
    craft: Optional[CraftSchema] = None
