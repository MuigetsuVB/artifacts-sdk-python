"""Multi-character example -- 5 fighters running simultaneously.

Each character loops through:
1. If HP < 40% -> rest
2. Otherwise -> fight the monster on the current map
3. Wait for cooldown
4. Repeat

All 5 loops run in parallel using asyncio.gather().
"""

import asyncio

from artifacts import ArtifactsClient, wait_for_cooldown
from artifacts.errors import (
    CooldownActiveError,
    ActionInProgressError,
    ContentNotOnMapError,
)

# Replace with your token
TOKEN = "your_token_here"

# Names of your 5 characters
CHARACTER_NAMES = [
    "Fighter1",
    "Fighter2",
    "Fighter3",
    "Fighter4",
    "Fighter5",
]

# Coordinates of a monster spot (e.g. chickens at 0,1)
FIGHT_X = 0
FIGHT_Y = 1

# Number of fights per character (0 = infinite)
MAX_FIGHTS = 20

# HP threshold for resting (percentage)
REST_THRESHOLD = 0.4


async def combat_loop(char, max_fights: int = MAX_FIGHTS):
    """Combat loop for a single character."""

    name = char.name
    fights_done = 0

    # Fetch initial state
    info = await char.get()
    print(f"[{name}] Starting lv{info.level} HP={info.hp}/{info.max_hp} pos=({info.x},{info.y})")

    # Move to the fight spot if needed
    if info.x != FIGHT_X or info.y != FIGHT_Y:
        print(f"[{name}] Moving to ({FIGHT_X},{FIGHT_Y})...")
        try:
            move_result = await char.move(x=FIGHT_X, y=FIGHT_Y)
            await wait_for_cooldown(move_result.cooldown)
        except CooldownActiveError:
            await asyncio.sleep(3)
            move_result = await char.move(x=FIGHT_X, y=FIGHT_Y)
            await wait_for_cooldown(move_result.cooldown)

    while True:
        # Check fight limit
        if max_fights > 0 and fights_done >= max_fights:
            print(f"[{name}] {max_fights} fights completed!")
            break

        # Fetch current HP
        info = await char.get()

        # Rest if HP is low
        if info.hp < info.max_hp * REST_THRESHOLD:
            print(f"[{name}] Low HP ({info.hp}/{info.max_hp}), resting...")
            try:
                rest_result = await char.rest()
                print(f"[{name}] +{rest_result.hp_restored} HP")
                await wait_for_cooldown(rest_result.cooldown)
            except CooldownActiveError:
                await asyncio.sleep(3)
            continue

        # Fight
        try:
            result = await char.fight()
        except CooldownActiveError:
            # Still in cooldown, wait a bit
            await asyncio.sleep(2)
            continue
        except ActionInProgressError:
            await asyncio.sleep(2)
            continue
        except ContentNotOnMapError:
            print(f"[{name}] No monster here, stopping.")
            break

        fight = result.fight
        char_result = fight.characters[0]
        fights_done += 1

        # Display result
        status = "WIN" if fight.result.value == "win" else "LOSS"
        print(
            f"[{name}] Fight #{fights_done}: {status} "
            f"({fight.turns} turns) +{char_result.xp}xp +{char_result.gold}g "
            f"HP={char_result.final_hp}"
        )

        # Display drops
        if char_result.drops:
            drops_str = ", ".join(
                f"{d.code}x{d.quantity}" for d in char_result.drops
            )
            print(f"[{name}]   Drops: {drops_str}")

        # Wait for cooldown before next fight
        await wait_for_cooldown(result.cooldown)

    # Final summary
    final = await char.get()
    print(f"[{name}] Done! lv{final.level} HP={final.hp}/{final.max_hp} gold={final.gold}")


async def main():
    async with ArtifactsClient(token=TOKEN) as client:
        print("=== Artifacts MMO -- Combat Loop (5 characters) ===\n")

        # Verify characters exist
        my_chars = await client.my_account.get_characters()
        my_names = {c.name for c in my_chars}

        active_names = []
        for name in CHARACTER_NAMES:
            if name in my_names:
                active_names.append(name)
            else:
                print(f"WARNING: character '{name}' not found, skipping.")

        if not active_names:
            print("No valid characters. Check CHARACTER_NAMES.")
            return

        print(f"Launching {len(active_names)} character(s) in parallel...\n")

        # Create controllers and launch loops in parallel
        chars = [client.character(name) for name in active_names]
        await asyncio.gather(*[combat_loop(c) for c in chars])

        print("\n=== All fights completed! ===")


if __name__ == "__main__":
    asyncio.run(main())
