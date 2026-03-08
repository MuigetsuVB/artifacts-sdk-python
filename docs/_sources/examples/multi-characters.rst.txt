Multi-Character Bots
=====================

Run multiple characters **at the same time** using async and
``asyncio.gather()``.

.. note::

   Multi-character requires the **async** client (``AsyncArtifactsClient``).
   If you're not familiar with async, check :doc:`first-bot` first.

5 Fighters in Parallel
------------------------

.. code-block:: python

   import asyncio
   from artifacts import AsyncArtifactsClient
   from artifacts.errors import ContentNotOnMapError

   TOKEN = "your_token_here"
   CHARACTERS = ["Fighter1", "Fighter2", "Fighter3", "Fighter4", "Fighter5"]
   FIGHT_X, FIGHT_Y = 0, 1
   MAX_FIGHTS = 20
   REST_THRESHOLD = 0.4

   async def combat_loop(char):
       """Combat loop for a single character."""
       name = char.name
       info = await char.get()
       print(f"[{name}] Level {info.level} HP {info.hp}/{info.max_hp}")

       # Move to fight spot
       if info.x != FIGHT_X or info.y != FIGHT_Y:
           await char.move(x=FIGHT_X, y=FIGHT_Y)

       fights = 0
       while fights < MAX_FIGHTS:
           info = await char.get()
           if info.hp < info.max_hp * REST_THRESHOLD:
               rest = await char.rest()
               print(f"[{name}] Rested +{rest.hp_restored} HP")
               continue

           try:
               result = await char.fight()
           except ContentNotOnMapError:
               print(f"[{name}] No monster, stopping.")
               break

           fight = result.fight
           cr = fight.characters[0]
           fights += 1
           print(f"[{name}] Fight #{fights}: {fight.result.value} +{cr.xp}xp")

       print(f"[{name}] Done! {fights} fights completed.")

   async def main():
       async with AsyncArtifactsClient(token=TOKEN) as client:
           print("=== Multi-Character Combat ===\n")

           # Verify characters exist
           my_chars = await client.my_account.get_characters()
           my_names = {c.name for c in my_chars}

           active = []
           for name in CHARACTERS:
               if name in my_names:
                   active.append(client.character(name))
               else:
                   print(f"WARNING: '{name}' not found, skipping.")

           if not active:
               print("No valid characters!")
               return

           # Run all combat loops in parallel
           await asyncio.gather(*[combat_loop(c) for c in active])
           print("\n=== All done! ===")

   asyncio.run(main())

How It Works
-------------

1. ``asyncio.gather()`` runs all character loops **simultaneously**
2. Each character has its own independent cooldown
3. While one character waits for a cooldown, others keep fighting
4. The SDK tracks cooldowns per-character automatically

Mixed Roles (Fighter + Gatherer)
----------------------------------

.. code-block:: python

   import asyncio
   from artifacts import AsyncArtifactsClient

   TOKEN = "your_token_here"

   async def fighter_loop(char):
       await char.move(x=0, y=1)
       for i in range(10):
           info = await char.get()
           if info.hp < info.max_hp * 0.4:
               await char.rest()
           result = await char.fight()
           print(f"[{char.name}] Fight {i+1}: {result.fight.result.value}")

   async def gatherer_loop(char):
       await char.move(x=2, y=0)
       for i in range(10):
           result = await char.skills.gather()
           print(f"[{char.name}] Gather {i+1}: +{result.xp}xp")

   async def main():
       async with AsyncArtifactsClient(token=TOKEN) as client:
           fighter = client.character("MyFighter")
           gatherer = client.character("MyGatherer")

           await asyncio.gather(
               fighter_loop(fighter),
               gatherer_loop(gatherer),
           )

   asyncio.run(main())

Tips
-----

- Each character can only do **one action at a time** (server-enforced)
- Use ``asyncio.gather()`` to run characters in parallel, not threads
- Shared cooldown tracking means no wasted time between actions
- Start with 2 characters and scale up once you're comfortable
