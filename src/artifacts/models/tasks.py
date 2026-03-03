from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import RewardsSchema
from .enums import Skill, TaskType


class TaskSchema(BaseModel):
    code: str
    type: TaskType
    total: int
    rewards: RewardsSchema


class TaskFullSchema(BaseModel):
    code: str
    level: int
    type: TaskType
    min_quantity: int
    max_quantity: int
    skill: Optional[Skill] = None
    rewards: RewardsSchema


class TaskTradeSchema(BaseModel):
    code: str
    quantity: int
