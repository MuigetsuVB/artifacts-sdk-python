from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .enums import AccountStatus, CharacterSkin


class AccountDetails(BaseModel):
    username: str
    member: bool
    status: AccountStatus
    badges: list[str]
    skins: list[CharacterSkin]
    achievements_points: int
    banned: bool
    ban_reason: Optional[str] = None


class MyAccountDetails(BaseModel):
    username: str
    email: str
    member: bool
    member_expiration: Optional[str] = None
    status: AccountStatus
    badges: list[str]
    skins: list[CharacterSkin]
    gems: int
    event_token: int
    achievements_points: int
    banned: bool
    ban_reason: Optional[str] = None
