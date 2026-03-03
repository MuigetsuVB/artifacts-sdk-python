from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import MapLayer


class EventContentSchema(BaseModel):
    type: str
    code: str


class EventMapSchema(BaseModel):
    map_id: int
    x: int
    y: int
    layer: MapLayer
    skin: Optional[str] = None


class EventSchema(BaseModel):
    name: str
    code: str
    content: EventContentSchema
    maps: list[EventMapSchema]
    duration: int
    rate: int


class ActiveEventSchema(BaseModel):
    name: str
    code: str
    map: EventMapSchema
    previous_map: Optional[EventMapSchema] = None
    duration: int
    expiration: str
    created_at: str
