from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import ConditionSchema
from .enums import MapAccessType, MapContentType, MapLayer


class MapContentSchema(BaseModel):
    type: MapContentType
    code: str


class TransitionSchema(BaseModel):
    map_id: int
    x: int
    y: int
    layer: MapLayer
    conditions: list[ConditionSchema]


class InteractionSchema(BaseModel):
    content: Optional[MapContentSchema] = None
    transition: Optional[TransitionSchema] = None


class AccessSchema(BaseModel):
    type: MapAccessType
    conditions: list[ConditionSchema]


class MapSchema(BaseModel):
    map_id: int
    name: Optional[str] = None
    skin: Optional[str] = None
    x: int
    y: int
    layer: MapLayer
    access: Optional[AccessSchema] = None
    interactions: list[InteractionSchema]
