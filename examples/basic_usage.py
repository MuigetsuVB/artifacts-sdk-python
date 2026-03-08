"""Basic example -- Artifacts SDK usage.

Demonstrates how to:
- Connect with a token
- Read character info
- Browse game data (items, monsters, maps)
- Perform actions with auto-cooldown (move, fight, rest)
- Use domain sub-objects (skills, bank, equipment)
"""

import asyncio

from artifacts import AsyncArtifactsClient

# Replace with your own JWT token
TOKEN = "your_token_here"


async def main():
    async with AsyncArtifactsClient(token=TOKEN) as client:

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
        chicken = await client.monsters.get("chicken")
        print(f"\nMonster: {chicken.name} lv{chicken.level} HP={chicken.hp}")

        items_page = await client.items.get_all(min_level=1, max_level=5, size=5)
        print(f"\nItems lv1-5 (total: {items_page.total}):")
        for item in items_page.data:
            print(f"  {item.code} -- {item.name} (lv{item.level}, {item.type.value})")

        # ---- Control a character ----
        char = client.character(characters[0].name)
        info = await char.get()
        print(f"\nControlling {info.name} lv{info.level}")

        # Move (auto-waits cooldown)
        print("Moving to (0, 1)...")
        await char.move(x=0, y=1)

        # Fight (auto-waits cooldown)
        print("Fighting...")
        fight_result = await char.fight()
        fight = fight_result.fight
        print(f"  Result: {fight.result.value} in {fight.turns} turns")
        for cr in fight.characters:
            print(f"  {cr.character_name}: +{cr.xp}xp +{cr.gold}g HP={cr.final_hp}")

        # Rest if HP is low
        updated = fight_result.characters[0]
        if updated.hp < updated.max_hp * 0.5:
            print("Resting...")
            rest_result = await char.rest()
            print(f"  +{rest_result.hp_restored} HP")

        # ---- Domain sub-objects ----
        # These are just examples -- uncomment if your character is
        # at the right location with the right items.

        # Craft an item:
        # await char.skills.craft(code="copper_ring", quantity=1)

        # Deposit gold in the bank:
        # await char.bank.deposit_gold(quantity=100)

        # Equip an item:
        # from artifacts.models.enums import ItemSlot
        # await char.equipment.equip(code="copper_ring", slot=ItemSlot.RING1)

        print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
