from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import RewardItemSchema
from .enums import AchievementType


class AchievementObjectiveSchema(BaseModel):
    type: AchievementType
    target: Optional[str] = None
    total: int


class AchievementRewardsSchema(BaseModel):
    gold: int
    items: list[RewardItemSchema]


class AchievementSchema(BaseModel):
    name: str
    code: str
    description: str
    points: int
    objectives: list[AchievementObjectiveSchema]
    rewards: AchievementRewardsSchema


class AccountAchievementObjectiveSchema(BaseModel):
    type: AchievementType
    target: Optional[str] = None
    progress: int
    total: int


class AccountAchievementSchema(BaseModel):
    name: str
    code: str
    description: str
    points: int
    objectives: list[AccountAchievementObjectiveSchema]
    rewards: AchievementRewardsSchema
    completed_at: Optional[str] = None
