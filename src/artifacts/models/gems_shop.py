from __future__ import annotations

from pydantic import BaseModel

from .enums import CharacterSkin, MapContentType


class GemShopSkinCatalogItemSchema(BaseModel):
    code: str
    name: str
    description: str
    price: int


class GemShopSpawnEventCatalogItemSchema(BaseModel):
    code: str
    name: str
    content_type: MapContentType
    content_code: str
    duration: int
    price: int


class GemShopSubscriptionCatalogItemSchema(BaseModel):
    code: str
    name: str
    duration_days: int
    price: int


class GemShopCustomDesignCatalogItemSchema(BaseModel):
    code: str
    name: str
    description: str
    price: int
    category: str
    unique_to_account: bool


class GemShopCatalogDataSchema(BaseModel):
    skins: list[GemShopSkinCatalogItemSchema]
    spawn_events: list[GemShopSpawnEventCatalogItemSchema]
    subscriptions: list[GemShopSubscriptionCatalogItemSchema]
    custom_designs: list[GemShopCustomDesignCatalogItemSchema]


class BuySkinResponseDataSchema(BaseModel):
    skins: list[CharacterSkin | str]
    skin: CharacterSkin | str
    gems: int


class GemShopSubscriptionResponseDataSchema(BaseModel):
    member: bool
    member_expiration: str
    gems: int
    cost: int


class GemShopCustomDesignPurchaseResponseDataSchema(BaseModel):
    code: str
    name: str
    gems: int
    cost: int
