from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.combat import CombatSimulationDataSchema, FakeCharacterSchema

if TYPE_CHECKING:
    from ..http import HttpClient


class SimulationAPI:
    """Combat simulation (member/founder required)."""

    def __init__(self, http: HttpClient):
        self._http = http

    async def fight(
        self,
        characters: list[FakeCharacterSchema],
        monster: str,
        iterations: int = 100,
    ) -> CombatSimulationDataSchema:
        """POST /simulation/fight_simulation"""
        body = {
            "characters": [c.model_dump(exclude_none=True) for c in characters],
            "monster": monster,
            "iterations": iterations,
        }
        return await self._http.post_model(
            "/simulation/fight_simulation",
            CombatSimulationDataSchema,
            json=body,
        )
