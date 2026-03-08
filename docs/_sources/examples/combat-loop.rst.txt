Combat Loop
============

A robust combat loop that fights monsters, handles errors, and
automatically rests when HP gets low.

Full Code
----------

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.errors import ContentNotOnMapError, InventoryFullError

   TOKEN = "your_token_here"
   CHAR_NAME = "MyFighter"
   FIGHT_X, FIGHT_Y = 0, 1   # chicken spot
   MAX_FIGHTS = 50
   REST_THRESHOLD = 0.4       # rest below 40% HP

   with ArtifactsClient(token=TOKEN) as client:
       char = client.character(CHAR_NAME)
       info = char.get()
       print(f"[{info.name}] Level {info.level} HP {info.hp}/{info.max_hp}")

       # Move to fight spot
       if info.x != FIGHT_X or info.y != FIGHT_Y:
           print(f"Moving to ({FIGHT_X}, {FIGHT_Y})...")
           char.move(x=FIGHT_X, y=FIGHT_Y)

       fights = 0
       while fights < MAX_FIGHTS:
           # Check HP
           info = char.get()
           if info.hp < info.max_hp * REST_THRESHOLD:
               print(f"Low HP ({info.hp}/{info.max_hp}), resting...")
               rest = char.rest()
               print(f"+{rest.hp_restored} HP")
               continue

           # Fight
           try:
               result = char.fight()
           except ContentNotOnMapError:
               print("No monster here, stopping.")
               break
           except InventoryFullError:
               print("Inventory full! Stopping.")
               break

           fight = result.fight
           cr = fight.characters[0]
           fights += 1

           status = "WIN" if fight.result.value == "win" else "LOSS"
           print(f"Fight #{fights}: {status} ({fight.turns}t) +{cr.xp}xp +{cr.gold}g")

           # Show drops
           if cr.drops:
               for d in cr.drops:
                   print(f"  Drop: {d.code} x{d.quantity}")

       final = char.get()
       print(f"\nDone! Level {final.level} — {final.gold} gold — {fights} fights")

Key Points
-----------

- **Auto-rest**: Checks HP before each fight and rests if below threshold
- **Error handling**: Stops gracefully if no monsters or inventory full
- **Configurable**: Change ``FIGHT_X/Y``, ``MAX_FIGHTS``, ``REST_THRESHOLD``

Tips
-----

- Find monster spots: ``client.maps.get_all(content_type="monster")``
- Fight higher-level monsters as your character levels up
- If you lose a fight, you still keep your XP but lose some HP

What's Next?
-------------

- :doc:`resource-farming` — Gather and craft instead of fighting
- :doc:`multi-characters` — Run 5 fighters in parallel
