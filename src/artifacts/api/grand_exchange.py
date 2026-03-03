from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..models.enums import GEOrderType
from ..models.grand_exchange import GEOrderSchema, GeOrderHistorySchema
from ..models.pagination import DataPage

if TYPE_CHECKING:
    from ..http import HttpClient


class GrandExchangeAPI:
    """Grand Exchange public endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_history(
        self,
        code: str,
        *,
        account: Optional[str] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[GeOrderHistorySchema]:
        """GET /grandexchange/history/{code}"""
        params = {"account": account, "page": page, "size": size}
        return await self._http.get_page(
            f"/grandexchange/history/{code}",
            GeOrderHistorySchema,
            params=params,
        )

    async def get_orders(
        self,
        *,
        code: Optional[str] = None,
        account: Optional[str] = None,
        type: Optional[GEOrderType] = None,
        page: int = 1,
        size: int = 50,
    ) -> DataPage[GEOrderSchema]:
        """GET /grandexchange/orders"""
        params = {
            "code": code,
            "account": account,
            "type": type,
            "page": page,
            "size": size,
        }
        return await self._http.get_page(
            "/grandexchange/orders", GEOrderSchema, params=params
        )

    async def get_order(self, id: str) -> GEOrderSchema:
        """GET /grandexchange/orders/{id}"""
        return await self._http.get_model(
            f"/grandexchange/orders/{id}", GEOrderSchema
        )
