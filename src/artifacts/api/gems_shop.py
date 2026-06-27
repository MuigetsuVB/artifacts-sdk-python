from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.events import ActiveEventSchema
from ..models.gems_shop import (
    BuySkinResponseDataSchema,
    GemShopCatalogDataSchema,
    GemShopCustomDesignPurchaseResponseDataSchema,
    GemShopSubscriptionResponseDataSchema,
)

if TYPE_CHECKING:
    from ..http import HttpClient


class GemsShopAPI:
    """Gems shop endpoints."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def get_catalog(self) -> GemShopCatalogDataSchema:
        """GET /gems_shop/"""
        return await self._http.get_model("/gems_shop/", GemShopCatalogDataSchema)

    async def buy_skin(self, code: str) -> BuySkinResponseDataSchema:
        """POST /gems_shop/skin"""
        return await self._http.post_model(
            "/gems_shop/skin",
            BuySkinResponseDataSchema,
            json={"code": code},
        )

    async def spawn_event(self, code: str) -> ActiveEventSchema:
        """POST /gems_shop/spawn_event"""
        return await self._http.post_model(
            "/gems_shop/spawn_event",
            ActiveEventSchema,
            json={"code": code},
        )

    async def buy_subscription(self) -> GemShopSubscriptionResponseDataSchema:
        """POST /gems_shop/subscription"""
        return await self._http.post_model(
            "/gems_shop/subscription",
            GemShopSubscriptionResponseDataSchema,
        )

    async def buy_custom_design(
        self, code: str
    ) -> GemShopCustomDesignPurchaseResponseDataSchema:
        """POST /gems_shop/buy_custom_design"""
        return await self._http.post_model(
            "/gems_shop/buy_custom_design",
            GemShopCustomDesignPurchaseResponseDataSchema,
            json={"code": code},
        )
