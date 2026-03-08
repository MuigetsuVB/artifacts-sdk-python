from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from .enums import NPCType


class SimpleNPCItem(BaseModel):
    code: str
    currency: str
    buy_price: Optional[int] = None
    sell_price: Optional[int] = None


class NPCSchema(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    type: NPCType
    items: List[SimpleNPCItem] = []


class NpcItemTransactionSchema(BaseModel):
    code: str
    quantity: int
    currency: str
    price: int
    total_price: int
