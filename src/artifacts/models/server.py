from __future__ import annotations

from pydantic import BaseModel

from .badges import SeasonSchema


class RateLimitSchema(BaseModel):
    type: str
    value: str


class StatusSchema(BaseModel):
    version: str
    server_time: str
    max_level: int
    max_skill_level: int
    characters_online: int
    season: SeasonSchema
    rate_limits: list[RateLimitSchema]
