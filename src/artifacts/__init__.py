"""Artifacts MMO SDK -- Python.

Quick start (no async/await needed)::

    from artifacts import ArtifactsClient

    with ArtifactsClient(token="your_token") as client:
        char = client.character("MyChar")
        char.move(x=0, y=1)
        result = char.fight()
        print(result.fight.result)

Async quick start::

    import asyncio
    from artifacts import AsyncArtifactsClient

    async def main():
        async with AsyncArtifactsClient(token="your_token") as client:
            char = client.character("MyChar")
            await char.move(x=0, y=1)
            result = await char.fight()
            print(result.fight.result)

    asyncio.run(main())
"""

from .client import AsyncArtifactsClient
from .sync_client import ArtifactsClient
from .character import Character
from .cooldown import cooldown_seconds, wait_for_cooldown
from .http import RetryConfig
from ._logging import setup_logging
from .models.pagination import DataPage
from .errors import (
    ActionInProgressError,
    AlreadyAtDestinationError,
    ArtifactsAPIError,
    ArtifactsError,
    CharacterNotFoundError,
    ConditionsNotMetError,
    ContentNotOnMapError,
    CooldownActiveError,
    EquipmentSlotError,
    GrandExchangeError,
    InsufficientGoldError,
    InventoryFullError,
    MapBlockedError,
    MemberRequiredError,
    NoPathError,
    NotFoundError,
    RetryExhaustedError,
    SkillLevelTooLowError,
    TaskError,
    ValidationError,
)

__all__ = [
    # Core
    "ArtifactsClient",
    "AsyncArtifactsClient",
    "Character",
    # Configuration
    "RetryConfig",
    "setup_logging",
    # Cooldown helpers
    "wait_for_cooldown",
    "cooldown_seconds",
    # Pagination
    "DataPage",
    # Errors
    "ArtifactsError",
    "ArtifactsAPIError",
    "ActionInProgressError",
    "AlreadyAtDestinationError",
    "CharacterNotFoundError",
    "ConditionsNotMetError",
    "ContentNotOnMapError",
    "CooldownActiveError",
    "EquipmentSlotError",
    "GrandExchangeError",
    "InsufficientGoldError",
    "InventoryFullError",
    "MapBlockedError",
    "MemberRequiredError",
    "NoPathError",
    "NotFoundError",
    "RetryExhaustedError",
    "SkillLevelTooLowError",
    "TaskError",
    "ValidationError",
]
