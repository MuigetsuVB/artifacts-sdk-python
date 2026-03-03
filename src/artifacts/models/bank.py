from __future__ import annotations

from pydantic import BaseModel


class BankSchema(BaseModel):
    slots: int
    expansions: int
    next_expansion_cost: int
    gold: int


class BankExtensionSchema(BaseModel):
    price: int
