from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import NPCType


class NPCSchema(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    type: NPCType


class NPCItem(BaseModel):
    code: str
    npc: str
    currency: Optional[str] = None
    buy_price: Optional[int] = None
    sell_price: Optional[int] = None


class NpcItemTransactionSchema(BaseModel):
    code: str
    quantity: int
    currency: str
    price: int
    total_price: int
