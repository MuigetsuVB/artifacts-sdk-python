Getting Started
===============

This guide shows you how to connect and perform your first actions
in just a few minutes.

Connecting
----------

There are two ways to use the SDK:

**Simple (synchronous)** — recommended for beginners:

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       # all your code here
       pass

**Async** — for advanced users or multi-character bots:

.. code-block:: python

   import asyncio
   from artifacts import AsyncArtifactsClient

   async def main():
       async with AsyncArtifactsClient(token="your_token") as client:
           # all your code here (use await)
           pass

   asyncio.run(main())

.. tip::

   In the sync version, you do **not** need to write ``await``.
   The SDK takes care of that for you.

List Your Characters
---------------------

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       characters = client.my_account.get_characters()
       for c in characters:
           print(f"{c.name} — level {c.level} — HP {c.hp}/{c.max_hp}")

Control a Character
--------------------

.. code-block:: python

   # Pick a character
   char = client.character("MyChar")

   # View its info
   info = char.get()
   print(f"{info.name} is at ({info.x}, {info.y})")
   print(f"HP: {info.hp}/{info.max_hp}")
   print(f"Gold: {info.gold}")

Move and Fight
---------------

.. code-block:: python

   # Go to (0, 1) — that's where the chickens are!
   char.move(x=0, y=1)

   # Fight the monster on the tile
   result = char.fight()
   fight = result.fight

   print(f"Result: {fight.result.value}")  # "win" or "loss"
   print(f"Turns: {fight.turns}")
   print(f"+{fight.characters[0].xp} XP")
   print(f"+{fight.characters[0].gold} gold")

   # Rest if HP is low
   updated = result.characters[0]
   if updated.hp < updated.max_hp * 0.5:
       rest = char.rest()
       print(f"+{rest.hp_restored} HP restored")

.. note::

   The SDK **automatically** waits for cooldowns between actions.
   You don't need to manage anything!

Browse Game Data
-----------------

The client gives you access to all public game data:

.. code-block:: python

   # Monster info
   chicken = client.monsters.get("chicken")
   print(f"{chicken.name} — level {chicken.level} — HP {chicken.hp}")

   # Search for items
   items = client.items.get_all(min_level=1, max_level=5, size=5)
   for item in items.data:
       print(f"{item.name} (level {item.level})")

   # Explore the map
   maps = client.maps.get_all(content_type="monster", size=5)
   for m in maps.data:
       print(f"({m.x}, {m.y}) — {m.content.code if m.content else '?'}")

Quick Reference
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - What you want to do
     - Code
   * - Connect
     - ``ArtifactsClient(token="...")``
   * - Pick a character
     - ``client.character("Name")``
   * - Move
     - ``char.move(x=0, y=1)``
   * - Fight
     - ``char.fight()``
   * - Rest
     - ``char.rest()``
   * - View character info
     - ``char.get()``
   * - Game data
     - ``client.monsters.get("chicken")``

Next Step
---------

Head to :doc:`character` to learn everything about character actions.
