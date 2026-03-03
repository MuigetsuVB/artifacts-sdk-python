from __future__ import annotations

from pydantic import BaseModel


class BadgeConditionSchema(BaseModel):
    code: str
    quantity: int


class BadgeSchema(BaseModel):
    code: str
    season: int
    description: str
    conditions: list[BadgeConditionSchema]


class SeasonBadgeSchema(BaseModel):
    code: str
    description: str
    required_points: int


class SeasonSkinSchema(BaseModel):
    code: str
    description: str
    required_points: int


class SeasonSchema(BaseModel):
    name: str
    number: int
    start_date: str
    badges: list[SeasonBadgeSchema]
    skins: list[SeasonSkinSchema]
