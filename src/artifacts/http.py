"""Low-level async HTTP transport for the Artifacts API."""

from __future__ import annotations

import asyncio
import base64
import json as _json
import logging
import random
import sys
from dataclasses import dataclass
from typing import Any, Optional, Type, TypeVar
from urllib.parse import urlencode

import pydantic
from pydantic import BaseModel

from .errors import ArtifactsAPIError, ArtifactsError, RetryExhaustedError, raise_for_error
from .models.pagination import DataPage

T = TypeVar("T", bound=BaseModel)

_PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2

logger = logging.getLogger("artifacts.http")


def _parse(model: Type[T], data: Any) -> T:
    """Parse *data* into *model*, compatible with pydantic v1 and v2."""
    if _PYDANTIC_V2:
        return model.model_validate(data)  # type: ignore[attr-defined]
    return model.parse_obj(data)  # type: ignore[attr-defined]


_PYODIDE = sys.platform == "emscripten"

if not _PYODIDE:
    import aiohttp


@dataclass
class RetryConfig:
    """Configuration for automatic request retries.

    Parameters
    ----------
    max_retries:
        Maximum number of retry attempts (default 3).
    base_delay:
        Initial delay in seconds before the first retry (default 1.0).
    max_delay:
        Maximum delay cap in seconds for exponential backoff (default 30.0).
    retry_on_status:
        HTTP status codes that trigger a retry.
    retry_on_cooldown:
        If ``True``, automatically wait and retry on ``CooldownActiveError``
        (status 499).
    """

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504)
    retry_on_cooldown: bool = True


class HttpClient:
    """Async HTTP client wrapping aiohttp (native) or pyodide.http.pyfetch (WebAssembly).

    Manages the session lifecycle and provides typed request helpers
    that automatically unwrap the ``{"data": ...}`` envelope returned
    by the Artifacts API.
    """

    def __init__(
        self,
        base_url: str = "https://api.artifactsmmo.com",
        token: Optional[str] = None,
        retry: Optional[RetryConfig] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._retry = retry or RetryConfig()
        self._headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._token:
            self._headers["Authorization"] = f"Bearer {self._token}"

        # Native-only: aiohttp session
        self._session: Optional[Any] = None

    # -- Lifecycle --

    async def start(self) -> None:
        """Create the underlying HTTP session (native only)."""
        if _PYODIDE:
            return
        self._session = aiohttp.ClientSession(
            base_url=self._base_url,
            headers=self._headers,
        )

    async def close(self) -> None:
        """Close the underlying session."""
        if _PYODIDE:
            return
        if self._session and not self._session.closed:
            await self._session.close()

    @property
    def session(self) -> Any:
        if _PYODIDE:
            raise ArtifactsError(
                "Direct session access is not available in Pyodide."
            )
        if self._session is None or self._session.closed:
            raise ArtifactsError(
                "HttpClient session is not started. "
                "Use 'async with AsyncArtifactsClient(...) as client:' "
                "or call 'await client.start()' first."
            )
        return self._session

    # -- Retry helpers --

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with 10 % jitter."""
        delay = min(self._retry.base_delay * (2 ** attempt), self._retry.max_delay)
        return delay + random.uniform(0, delay * 0.1)

    @staticmethod
    def _extract_cooldown_seconds(exc: ArtifactsAPIError) -> float:
        """Extract remaining cooldown from error data, with a safe fallback."""
        if exc.data and "remaining_seconds" in exc.data:
            return float(exc.data["remaining_seconds"])
        return 3.0

    # -- Low-level request --

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[dict[str, Any]] = None,
        auth: Optional[tuple[str, str]] = None,
    ) -> dict[str, Any]:
        """Send a request and return the raw JSON response dict.

        Includes automatic retry with exponential backoff for transient
        errors, rate limits (429), and cooldown conflicts (499).

        Parameters
        ----------
        auth:
            Optional ``(username, password)`` tuple for HTTP Basic auth.

        Raises :class:`ArtifactsAPIError` (or a subclass) on non-2xx
        responses, or :class:`RetryExhaustedError` when all retries
        are exhausted.
        """
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exc: ArtifactsAPIError | None = None

        for attempt in range(self._retry.max_retries + 1):
            try:
                logger.debug("%s %s (attempt %d)", method, path, attempt + 1)

                if _PYODIDE:
                    return await self._request_pyodide(
                        method, path, json=json, params=params, auth=auth
                    )
                return await self._request_native(
                    method, path, json=json, params=params, auth=auth
                )

            except ArtifactsAPIError as exc:
                last_exc = exc

                # No retries left → re-raise
                if attempt >= self._retry.max_retries:
                    break

                # Rate-limit (429)
                if exc.code == 429:
                    delay = self._backoff_delay(attempt)
                    logger.warning(
                        "Rate limited on %s %s, retrying in %.1fs (attempt %d/%d)",
                        method, path, delay, attempt + 1, self._retry.max_retries,
                    )
                    await asyncio.sleep(delay)
                    continue

                # Cooldown active (499)
                if exc.code == 499 and self._retry.retry_on_cooldown:
                    cd_secs = self._extract_cooldown_seconds(exc)
                    logger.debug(
                        "Cooldown active on %s %s, waiting %.1fs",
                        method, path, cd_secs,
                    )
                    await asyncio.sleep(cd_secs)
                    continue

                # Server errors (500, 502, 503, 504)
                if exc.code in self._retry.retry_on_status:
                    delay = self._backoff_delay(attempt)
                    logger.warning(
                        "Server error %d on %s %s, retrying in %.1fs (attempt %d/%d)",
                        exc.code, method, path, delay,
                        attempt + 1, self._retry.max_retries,
                    )
                    await asyncio.sleep(delay)
                    continue

                # Non-retryable error → raise immediately
                raise

        # All retries exhausted
        if last_exc is not None:
            raise RetryExhaustedError(
                f"Request {method} {path} failed after {self._retry.max_retries + 1} attempts",
                last_exception=last_exc,
            )
        raise ArtifactsError("Unexpected retry loop exit")  # pragma: no cover

    async def _request_native(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[dict[str, Any]] = None,
        auth: Optional[tuple[str, str]] = None,
    ) -> dict[str, Any]:
        """Send a request using aiohttp (native Python)."""
        aiohttp_auth = None
        if auth:
            aiohttp_auth = aiohttp.BasicAuth(auth[0], auth[1])

        resp = await self.session.request(
            method,
            path,
            json=json,
            params=params,
            auth=aiohttp_auth,
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

    async def _request_pyodide(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[dict[str, Any]] = None,
        auth: Optional[tuple[str, str]] = None,
    ) -> dict[str, Any]:
        """Send a request using pyodide.http.pyfetch (WebAssembly)."""
        from pyodide.http import pyfetch  # type: ignore[import-not-found]

        headers = dict(self._headers)
        if auth:
            cred = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
            headers["Authorization"] = f"Basic {cred}"

        url = f"{self._base_url}{path}"
        if params:
            url += "?" + urlencode(params)

        kwargs: dict[str, Any] = {"method": method, "headers": headers}
        if json is not None:
            kwargs["body"] = _json.dumps(json)

        resp = await pyfetch(url, **kwargs)

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
        auth: Optional[tuple[str, str]] = None,
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
        return _parse(model, data["data"])

    async def post_model(
        self,
        path: str,
        model: Type[T],
        *,
        json: Any = None,
        auth: Optional[tuple[str, str]] = None,
    ) -> T:
        """POST, unwrap ``{"data": ...}``, parse into *model*."""
        data = await self.post(path, json=json, auth=auth)
        return _parse(model, data["data"])

    async def get_page(
        self,
        path: str,
        item_model: Type[T],
        *,
        params: Optional[dict[str, Any]] = None,
    ) -> DataPage[T]:
        """GET a paginated endpoint and return a typed ``DataPage``."""
        raw = await self.get(path, params=params)
        items = [_parse(item_model, x) for x in raw["data"]]
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
