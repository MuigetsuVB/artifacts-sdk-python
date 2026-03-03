from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import AccountLeaderboardType, AccountStatus, CharacterSkin


class CharacterLeaderboardSchema(BaseModel):
    position: int
    name: str
    account: str
    status: AccountStatus
    skin: CharacterSkin
    level: int
    total_xp: int
    mining_level: int
    mining_total_xp: int
    woodcutting_level: int
    woodcutting_total_xp: int
    fishing_level: int
    fishing_total_xp: int
    weaponcrafting_level: int
    weaponcrafting_total_xp: int
    gearcrafting_level: int
    gearcrafting_total_xp: int
    jewelrycrafting_level: int
    jewelrycrafting_total_xp: int
    cooking_level: int
    cooking_total_xp: int
    alchemy_level: int
    alchemy_total_xp: int
    gold: int


class AccountLeaderboardSchema(BaseModel):
    position: int
    account: str
    status: AccountStatus
    achievements_points: int
    gold: int
