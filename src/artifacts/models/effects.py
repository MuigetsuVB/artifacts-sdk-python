from __future__ import annotations

from pydantic import BaseModel

from .enums import EffectSubtype, EffectType


class EffectSchema(BaseModel):
    name: str
    code: str
    description: str
    type: EffectType
    subtype: EffectSubtype
