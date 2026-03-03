"""Low-level async HTTP transport for the Artifacts API."""

from __future__ import annotations

import asyncio
from typing import Any, Optional, Type, TypeVar

import aiohttp
from pydantic import BaseModel

from .errors import ArtifactsError, raise_for_error
from .models.pagination import DataPage

T = TypeVar("T", bound=BaseModel)


class HttpClient:
    """Async HTTP client wrapping aiohttp.

    Manages the session lifecycle and provides typed request helpers
    that automatically unwrap the ``{"data": ...}`` envelope returned
    by the Artifacts API.
    """

    def __init__(
        self,
        base_url: str = "https://api.artifactsmmo.com",
        token: Optional[str] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._session: Optional[aiohttp.ClientSession] = None

    # -- Lifecycle --

    async def start(self) -> None:
        """Create the underlying ``aiohttp.ClientSession``."""
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        self._session = aiohttp.ClientSession(
            base_url=self._base_url,
            headers=headers,
        )

    async def close(self) -> None:
        """Close the underlying session."""
        if self._session and not self._session.closed:
            await self._session.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            raise ArtifactsError(
                "HttpClient session is not started. "
                "Use 'async with ArtifactsClient(...) as client:' "
                "or call 'await client.start()' first."
            )
        return self._session

    # -- Low-level request --

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[dict[str, Any]] = None,
        auth: Optional[aiohttp.BasicAuth] = None,
    ) -> dict[str, Any]:
        """Send a request and return the raw JSON response dict.

        Raises :class:`ArtifactsAPIError` (or a subclass) on non-2xx
        responses.
        """
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        resp = await self.session.request(
            method,
            path,
            json=json,
            params=params,
            auth=auth,
        )

        if resp.status >= 400:
            try:
                body = await resp.json()
            except Exception:
                body = {}
            raise_for_error(resp.status, body)

        if resp.status == 204:
            return {}

        return await resp.json()

    # -- Convenience shortcuts --

    async def get(
        self,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json: Any = None,
        auth: Optional[aiohttp.BasicAuth] = None,
    ) -> dict[str, Any]:
        return await self.request("POST", path, json=json, auth=auth)

    # -- Typed helpers (unwrap .data automatically) --

    async def get_model(
        self,
        path: str,
        model: Type[T],
        *,
        params: Optional[dict[str, Any]] = None,
    ) -> T:
        """GET, unwrap ``{"data": ...}``, parse into *model*."""
        data = await self.get(path, params=params)
        return model.model_validate(data["data"])

    async def post_model(
        self,
        path: str,
        model: Type[T],
        *,
        json: Any = None,
        auth: Optional[aiohttp.BasicAuth] = None,
    ) -> T:
        """POST, unwrap ``{"data": ...}``, parse into *model*."""
        data = await self.post(path, json=json, auth=auth)
        return model.model_validate(data["data"])

    async def get_page(
        self,
        path: str,
        item_model: Type[T],
        *,
        params: Optional[dict[str, Any]] = None,
    ) -> DataPage[T]:
        """GET a paginated endpoint and return a typed ``DataPage``."""
        raw = await self.get(path, params=params)
        items = [item_model.model_validate(x) for x in raw["data"]]
        return DataPage(
            data=items,
            total=raw["total"],
            page=raw["page"],
            size=raw["size"],
            pages=raw["pages"],
        )

    async def get_all_pages(
        self,
        path: str,
        item_model: Type[T],
        *,
        params: Optional[dict[str, Any]] = None,
        page_size: int = 100,
    ) -> list[T]:
        """Fetch *all* pages of a paginated endpoint and return a flat list."""
        if params is None:
            params = {}
        params["size"] = page_size
        params["page"] = 1

        first = await self.get_page(path, item_model, params=params)
        all_items: list[T] = list(first.data)

        if first.pages <= 1:
            return all_items

        # Fetch remaining pages concurrently
        async def _fetch_page(p: int) -> list[T]:
            page_params = {**params, "page": p}
            page_result = await self.get_page(path, item_model, params=page_params)
            return list(page_result.data)

        remaining = await asyncio.gather(
            *[_fetch_page(p) for p in range(2, first.pages + 1)]
        )
        for page_items in remaining:
            all_items.extend(page_items)

        return all_items
