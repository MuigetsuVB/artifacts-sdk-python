from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import SimpleEffectSchema
from .enums import MonsterType


class DropRateSchema(BaseModel):
    code: str
    rate: int
    min_quantity: int
    max_quantity: int


class MonsterSchema(BaseModel):
    name: str
    code: str
    level: int
    type: MonsterType
    hp: int
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    critical_strike: int
    initiative: int
    effects: list[SimpleEffectSchema]
    min_gold: int
    max_gold: int
    drops: list[DropRateSchema]
