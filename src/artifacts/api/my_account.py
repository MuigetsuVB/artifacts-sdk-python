from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any

from ..models.account import MyAccountDetails
from ..models.bank import BankSchema
from ..models.character import CharacterSchema
from ..models.common import SimpleItemSchema
from ..models.enums import GEOrderType
from ..models.grand_exchange import GEOrderSchema, GeOrderHistorySchema
from ..models.logs import LogSchema, PendingItemSchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class MyAccountAPI:
    """Authenticated account endpoints (/my/...)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_details(self) -> MyAccountDetails:
        """GET /my/details"""
        return await self._http.get_model("/my/details", MyAccountDetails)

    async def get_bank(self) -> BankSchema:
        """GET /my/bank"""
        return await self._http.get_model("/my/bank", BankSchema)

    async def get_bank_items(
        self,
        *,
        item_code: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[SimpleItemSchema]:
        """GET /my/bank/items"""
        params = {"item_code": item_code, "page": page, "size": size}
        return await self._http.get_page(
            "/my/bank/items", SimpleItemSchema, params=params
        )

    async def get_ge_orders(
        self,
        *,
        code: Optional[str] = None,
        type: Optional[GEOrderType] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[GEOrderSchema]:
        """GET /my/grandexchange/orders"""
        params = {"code": code, "type": type, "page": page, "size": size}
        return await self._http.get_page(
            "/my/grandexchange/orders", GEOrderSchema, params=params
        )

    async def get_ge_history(
        self,
        *,
        id: Optional[str] = None,
        code: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[GeOrderHistorySchema]:
        """GET /my/grandexchange/history"""
        params = {"id": id, "code": code, "page": page, "size": size}
        return await self._http.get_page(
            "/my/grandexchange/history", GeOrderHistorySchema, params=params
        )

    async def get_pending_items(
        self,
        *,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[PendingItemSchema]:
        """GET /my/pending_items"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            "/my/pending_items", PendingItemSchema, params=params
        )

    async def change_password(
        self, current_password: str, new_password: str
    ) -> str:
        """POST /my/change_password"""
        data = await self._http.post(
            "/my/change_password",
            json={
                "current_password": current_password,
                "new_password": new_password,
            },
        )
        return data.get("message", "OK")

    async def change_email(self, current_email: str, new_email: str) -> str:
        """POST /my/change_email"""
        data = await self._http.post(
            "/my/change_email",
            json={"current_email": current_email, "new_email": new_email},
        )
        return data.get("message", "OK")

    async def get_gems_history(self) -> dict[str, Any]:
        """GET /my/gems_history"""
        return await self._http.get("/my/gems_history")

    async def get_purchase_history(self) -> dict[str, Any]:
        """GET /my/purchase_history"""
        return await self._http.get("/my/purchase_history")

    async def get_rates(self) -> dict[str, Any]:
        """GET /my/rates"""
        return await self._http.get("/my/rates")

    async def get_subscription(self) -> dict[str, Any]:
        """GET /my/subscription"""
        return await self._http.get("/my/subscription")

    async def buy_gems(self, quantity: int) -> dict[str, Any]:
        """POST /my/buy_gems"""
        return await self._http.post("/my/buy_gems", json={"quantity": quantity})

    async def subscribe_stripe(self, plan: str) -> dict[str, Any]:
        """POST /my/subscribe/stripe"""
        return await self._http.post(
            "/my/subscribe/stripe",
            json={"plan": plan},
        )

    async def subscribe_member_token(self) -> dict[str, Any]:
        """POST /my/subscribe/member_token"""
        return await self._http.post("/my/subscribe/member_token")

    async def cancel_subscription(self) -> str:
        """POST /my/subscribe/cancel"""
        data = await self._http.post("/my/subscribe/cancel")
        return data.get("message", "OK")

    async def get_characters(self) -> list[CharacterSchema]:
        """GET /my/characters"""
        data = await self._http.get("/my/characters")
        return [CharacterSchema.model_validate(c) for c in data["data"]]

    async def get_all_logs(
        self,
        *,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[LogSchema]:
        """GET /my/logs"""
        params = {"page": page, "size": size}
        return await self._http.get_page("/my/logs", LogSchema, params=params)
