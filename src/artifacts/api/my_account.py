from __future__ import annotations

from typing import Optional, TYPE_CHECKING

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
        """GET /my/pending-items"""
        params = {"page": page, "size": size}
        return await self._http.get_page(
            "/my/pending-items", PendingItemSchema, params=params
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
