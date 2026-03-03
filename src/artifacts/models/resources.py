from __future__ import annotations

from pydantic import BaseModel

from .enums import GatheringSkill
from .monsters import DropRateSchema


class ResourceSchema(BaseModel):
    name: str
    code: str
    skill: GatheringSkill
    level: int
    drops: list[DropRateSchema]
