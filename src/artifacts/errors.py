"""Exception hierarchy for the Artifacts wrapper."""

from __future__ import annotations

from typing import Any, Optional


class ArtifactsError(Exception):
    """Base exception for all artifacts wrapper errors."""


class ArtifactsAPIError(ArtifactsError):
    """The API returned an error response."""

    def __init__(
        self,
        code: int,
        message: str,
        data: Optional[dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}")


class CharacterNotFoundError(ArtifactsAPIError):
    """Character not found (498)."""


class CooldownActiveError(ArtifactsAPIError):
    """Character is in cooldown (499)."""


class ActionInProgressError(ArtifactsAPIError):
    """An action is already in progress (486)."""


class NotFoundError(ArtifactsAPIError):
    """Resource not found (404)."""


class InventoryFullError(ArtifactsAPIError):
    """Character inventory is full (497)."""


class InsufficientGoldError(ArtifactsAPIError):
    """Not enough gold (492)."""


class AlreadyAtDestinationError(ArtifactsAPIError):
    """Already at destination (490)."""


class SkillLevelTooLowError(ArtifactsAPIError):
    """Skill level too low (493)."""


class EquipmentSlotError(ArtifactsAPIError):
    """Equipment slot error (491)."""


class MemberRequiredError(ArtifactsAPIError):
    """Member / founder required (451)."""


class MapBlockedError(ArtifactsAPIError):
    """Map is blocked (596)."""


class NoPathError(ArtifactsAPIError):
    """No path to destination (595)."""


class ContentNotOnMapError(ArtifactsAPIError):
    """Content not found on map (598)."""


class TaskError(ArtifactsAPIError):
    """Task-related error (474-489)."""


class GrandExchangeError(ArtifactsAPIError):
    """Grand Exchange error (433-438)."""


class ValidationError(ArtifactsAPIError):
    """Request validation error (422)."""


class ConditionsNotMetError(ArtifactsAPIError):
    """Conditions not met (496)."""


# Map API error codes to exception classes
ERROR_MAP: dict[int, type[ArtifactsAPIError]] = {
    404: NotFoundError,
    422: ValidationError,
    433: GrandExchangeError,
    434: GrandExchangeError,
    435: GrandExchangeError,
    436: GrandExchangeError,
    437: GrandExchangeError,
    438: GrandExchangeError,
    451: MemberRequiredError,
    474: TaskError,
    475: TaskError,
    486: ActionInProgressError,
    487: TaskError,
    488: TaskError,
    489: TaskError,
    490: AlreadyAtDestinationError,
    491: EquipmentSlotError,
    492: InsufficientGoldError,
    493: SkillLevelTooLowError,
    496: ConditionsNotMetError,
    497: InventoryFullError,
    498: CharacterNotFoundError,
    499: CooldownActiveError,
    595: NoPathError,
    596: MapBlockedError,
    598: ContentNotOnMapError,
}


def raise_for_error(status: int, body: dict[str, Any]) -> None:
    """Parse an error response body and raise the appropriate exception."""
    error_data = body.get("error", {})
    code = error_data.get("code", status)
    message = error_data.get("message", "Unknown error")
    data = error_data.get("data")
    exc_class = ERROR_MAP.get(code, ArtifactsAPIError)
    raise exc_class(code=code, message=message, data=data)
