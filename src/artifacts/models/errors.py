from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None
