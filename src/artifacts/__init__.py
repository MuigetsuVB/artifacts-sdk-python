"""Artifacts MMO API -- async Python wrapper.

Quick start::

    import asyncio
    from artifacts import ArtifactsClient, wait_for_cooldown

    async def main():
        async with ArtifactsClient(token="your_token") as client:
            char = client.character("MyChar")
            info = await char.get()
            print(f"{info.name} lv{info.level} HP={info.hp}/{info.max_hp}")

            result = await char.fight()
            print(result.fight.result)
            await wait_for_cooldown(result.cooldown)

    asyncio.run(main())
"""

from .client import ArtifactsClient
from .character import Character
from .cooldown import cooldown_seconds, wait_for_cooldown
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
    SkillLevelTooLowError,
    TaskError,
    ValidationError,
)

__all__ = [
    # Core
    "ArtifactsClient",
    "Character",
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
    "SkillLevelTooLowError",
    "TaskError",
    "ValidationError",
]
