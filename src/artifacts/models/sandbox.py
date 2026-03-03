from __future__ import annotations

from pydantic import BaseModel

from .common import CooldownSchema, SimpleItemSchema
from .character import CharacterSchema
from .enums import XPType


class SandboxGiveGoldDataSchema(BaseModel):
    cooldown: CooldownSchema
    quantity: int
    character: CharacterSchema


class SandboxGiveItemDataSchema(BaseModel):
    cooldown: CooldownSchema
    item: SimpleItemSchema
    character: CharacterSchema


class SandboxGiveXPDataSchema(BaseModel):
    cooldown: CooldownSchema
    type: XPType
    amount: int
    character: CharacterSchema
