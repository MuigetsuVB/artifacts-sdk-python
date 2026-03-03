from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import GEOrderType


class GEOrderSchema(BaseModel):
    id: str
    code: str
    created_at: str
    type: GEOrderType
    account: str
    quantity: int
    price: int


class GEOrderCreatedSchema(BaseModel):
    id: str
    created_at: str
    code: str
    quantity: int
    price: int
    total_price: int


class GETransactionSchema(BaseModel):
    id: str
    code: str
    quantity: int
    price: int
    total_price: int


class GeOrderHistorySchema(BaseModel):
    order_id: str
    seller: str
    buyer: str
    code: str
    quantity: int
    price: int
    sold_at: str
