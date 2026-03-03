from __future__ import annotations

from pydantic import BaseModel

from .combat import FakeCharacterSchema


class CombatSimulationRequestSchema(BaseModel):
    characters: list[FakeCharacterSchema]
    monster: str
    iterations: int = 100
