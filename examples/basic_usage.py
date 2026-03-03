"""Basic example -- Artifacts wrapper usage.

Demonstrates how to:
- Connect with a token
- Read character info
- Browse game data (items, monsters, maps)
- Perform simple actions (move, fight, rest)
"""

import asyncio

from artifacts import ArtifactsClient, wait_for_cooldown

# Replace with your own JWT token
TOKEN = "your_token_here"


async def main():
    async with ArtifactsClient(token=TOKEN) as client:

        # ---- Server status ----
        status = await client.server.get_status()
        print(f"Server v{status.version} -- {status.characters_online} players online")

        # ---- Account info ----
        account = await client.my_account.get_details()
        print(f"Account: {account.username} (status={account.status.value})")

        # ---- List your characters ----
        characters = await client.my_account.get_characters()
        for c in characters:
            print(f"  {c.name} lv{c.level} HP={c.hp}/{c.max_hp} pos=({c.x},{c.y})")

        # ---- Game data ----
        # Look up a monster
        chicken = await client.monsters.get("chicken")
        print(f"\nMonster: {chicken.name} lv{chicken.level} HP={chicken.hp}")

        # List items within a level range
        items_page = await client.items.get_all(min_level=1, max_level=5, size=5)
        print(f"\nItems lv1-5 (total: {items_page.total}):")
        for item in items_page.data:
            print(f"  {item.code} -- {item.name} (lv{item.level}, {item.type.value})")

        # Find a map that contains a specific monster
        maps_page = await client.maps.get_all(content_type="monster", content_code="chicken", size=1)
        if maps_page.data:
            m = maps_page.data[0]
            print(f"\nChicken can be found at ({m.x},{m.y})")

        # ---- Control a character ----
        char = client.character(characters[0].name)
        info = await char.get()
        print(f"\nControlling {info.name} lv{info.level}")

        # Move
        print("Moving to (0, 1)...")
        move_result = await char.move(x=0, y=1)
        print(f"  Cooldown: {move_result.cooldown.total_seconds}s")
        await wait_for_cooldown(move_result.cooldown)

        # Fight
        print("Fighting...")
        fight_result = await char.fight()
        fight = fight_result.fight
        print(f"  Result: {fight.result.value} in {fight.turns} turns")
        for cr in fight.characters:
            print(f"  {cr.character_name}: +{cr.xp}xp +{cr.gold}g remaining HP={cr.final_hp}")
        await wait_for_cooldown(fight_result.cooldown)

        # Rest if HP is low
        updated = fight_result.characters[0]
        if updated.hp < updated.max_hp * 0.5:
            print("Resting...")
            rest_result = await char.rest()
            print(f"  +{rest_result.hp_restored} HP")
            await wait_for_cooldown(rest_result.cooldown)

        print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
