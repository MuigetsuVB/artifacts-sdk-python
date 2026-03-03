from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import SimpleItemSchema
from .enums import PendingItemSource, LogType


class LogSchema(BaseModel):
    character: str
    account: str
    type: LogType
    description: str
    content: Optional[dict] = None
    cooldown: int
    cooldown_expiration: Optional[str] = None
    created_at: str


class PendingItemSchema(BaseModel):
    id: str
    account: str
    source: PendingItemSource
    source_id: Optional[str] = None
    description: Optional[str] = None
    gold: int
    items: list[SimpleItemSchema]
    created_at: str
    claimed_at: Optional[str] = None
