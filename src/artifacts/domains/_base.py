"""Base class for character domain controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

if TYPE_CHECKING:
    from ..http import HttpClient


class CharacterDomain:
    """Base class for all character sub-domain controllers.

    Each domain groups related character actions (bank, skills, etc.)
    into a cohesive namespace attached to a :class:`Character` instance.
    """

    def __init__(
        self,
        name: str,
        http: HttpClient,
        *,
        auto_wait: Union[bool, list] = True,
        cooldown_ref: List[Optional[float]],
    ):
        self._name = name
        self._http = http
        self._base = f"/my/{name}/action"
        # Accept either a plain bool (per-character override) or a shared
        # mutable list[bool] coming from the client so that changes to
        # ``client.auto_wait`` propagate instantly to all active instances.
        self._auto_wait_source: Union[bool, list] = (
            auto_wait if isinstance(auto_wait, list) else [auto_wait]
        )
        # Shared cooldown expiry timestamp (monotonic) across all domains of
        # a character.  None means no pending cooldown.
        self._cooldown_ref: List[Optional[float]] = cooldown_ref

    @property
    def _auto_wait(self) -> bool:
        return self._auto_wait_source[0]

    @_auto_wait.setter
    def _auto_wait(self, value: bool) -> None:
        self._auto_wait_source[0] = value

    @property
    def _cooldown_until(self) -> Optional[float]:
        return self._cooldown_ref[0]

    @_cooldown_until.setter
    def _cooldown_until(self, value: Optional[float]) -> None:
        self._cooldown_ref[0] = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._name!r})"
