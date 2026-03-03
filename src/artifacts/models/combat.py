from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import DropSchema
from .enums import FightResult


class CharacterMultiFightResultSchema(BaseModel):
    character_name: str
    xp: int
    gold: int
    drops: list[DropSchema]
    final_hp: int


class CharacterFightSchema(BaseModel):
    result: FightResult
    turns: int
    opponent: str
    logs: list[str]
    characters: list[CharacterMultiFightResultSchema]


class FakeCharacterSchema(BaseModel):
    level: int
    weapon_slot: Optional[str] = None
    rune_slot: Optional[str] = None
    shield_slot: Optional[str] = None
    helmet_slot: Optional[str] = None
    body_armor_slot: Optional[str] = None
    leg_armor_slot: Optional[str] = None
    boots_slot: Optional[str] = None
    ring1_slot: Optional[str] = None
    ring2_slot: Optional[str] = None
    amulet_slot: Optional[str] = None
    artifact1_slot: Optional[str] = None
    artifact2_slot: Optional[str] = None
    artifact3_slot: Optional[str] = None
    utility1_slot: Optional[str] = None
    utility2_slot: Optional[str] = None
    utility1_slot_quantity: int = 1
    utility2_slot_quantity: int = 1


class CombatResultSchema(BaseModel):
    result: FightResult
    turns: int
    logs: list[str]
    character_results: list[CharacterMultiFightResultSchema]


class CombatSimulationDataSchema(BaseModel):
    results: list[CombatResultSchema]
    wins: int
    losses: int
    winrate: float
