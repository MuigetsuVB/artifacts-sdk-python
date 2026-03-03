from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class DataPage(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    data: list[T]
    total: int
    page: int
    size: int
    pages: int
