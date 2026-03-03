from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.account import AccountDetails
from ..models.achievements import AccountAchievementSchema
from ..models.character import CharacterSchema
from ..models.enums import AchievementType
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class AccountsAPI:
    """Public account endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def create(self, username: str, password: str, email: str) -> str:
        """POST /accounts/create -- create a new account.

        Returns the server message.
        """
        data = await self._http.post(
            "/accounts/create",
            json={"username": username, "password": password, "email": email},
        )
        return data.get("message", "OK")

    async def forgot_password(self, email: str) -> str:
        """POST /accounts/forgot_password -- request password reset."""
        data = await self._http.post(
            "/accounts/forgot_password",
            json={"email": email},
        )
        return data.get("message", "OK")

    async def reset_password(self, token: str, new_password: str) -> str:
        """POST /accounts/reset_password -- reset with token."""
        data = await self._http.post(
            "/accounts/reset_password",
            json={"token": token, "new_password": new_password},
        )
        return data.get("message", "OK")

    async def get(self, account: str) -> AccountDetails:
        """GET /accounts/{account} -- retrieve account info."""
        return await self._http.get_model(
            f"/accounts/{account}", AccountDetails
        )

    async def get_achievements(
        self,
        account: str,
        *,
        type: Optional[AchievementType] = None,
        completed: Optional[bool] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[AccountAchievementSchema]:
        """GET /accounts/{account}/achievements"""
        params = {
            "type": type,
            "completed": completed,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            f"/accounts/{account}/achievements",
            AccountAchievementSchema,
            params=params,
        )

    async def get_characters(self, account: str) -> list[CharacterSchema]:
        """GET /accounts/{account}/characters"""
        data = await self._http.get(f"/accounts/{account}/characters")
        return [CharacterSchema.model_validate(c) for c in data["data"]]
