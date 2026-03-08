Your First Bot
===============

Let's build a simple bot that connects, moves to a monster spot,
fights a few times, and rests when HP gets low.

Full Code
----------

.. code-block:: python

   from artifacts import ArtifactsClient

   TOKEN = "your_token_here"

   with ArtifactsClient(token=TOKEN) as client:
       # Check server status
       status = client.server.get_status()
       print(f"Server v{status.version} — {status.characters_online} online")

       # Pick your first character
       characters = client.my_account.get_characters()
       char = client.character(characters[0].name)

       info = char.get()
       print(f"Playing as {info.name} (level {info.level})")

       # Move to chicken spot (0, 1)
       print("Moving to (0, 1)...")
       char.move(x=0, y=1)

       # Fight 5 times
       for i in range(5):
           result = char.fight()
           fight = result.fight
           cr = fight.characters[0]
           print(f"Fight {i+1}: {fight.result.value} — +{cr.xp}xp +{cr.gold}g")

           # Rest if HP is below 50%
           updated = result.characters[0]
           if updated.hp < updated.max_hp * 0.5:
               rest = char.rest()
               print(f"  Rested: +{rest.hp_restored} HP")

       print("Done!")

How It Works
-------------

1. **Connect**: ``ArtifactsClient(token=...)`` opens a connection
2. **Pick a character**: ``client.character("Name")`` gives you a controller
3. **Move**: ``char.move(x=0, y=1)`` walks your character to that tile
4. **Fight**: ``char.fight()`` starts combat with whatever monster is there
5. **Rest**: ``char.rest()`` recovers HP

.. note::

   All cooldowns are handled automatically. Each call blocks until
   the action is complete and ready for the next one.

What's Next?
-------------

- :doc:`combat-loop` — A smarter combat loop with error handling
- :doc:`resource-farming` — Gather resources and craft items
- :doc:`multi-characters` — Run multiple characters at once
