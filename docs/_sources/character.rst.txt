Your Character
===============

The character is your **main controller** in the game.
It moves, fights, gathers, crafts...

Create a Controller
--------------------

.. code-block:: python

   char = client.character("MyChar")

This doesn't create a new character in the game — it just gives
you a remote control for an existing one.

Direct Actions
---------------

Movement
^^^^^^^^

.. code-block:: python

   # By coordinates
   char.move(x=0, y=1)

   # By map ID
   char.move(map_id=42)

   # Transition (enter building, go underground, etc.)
   char.transition()

Combat
^^^^^^

.. code-block:: python

   # Simple fight
   result = char.fight()
   fight = result.fight

   print(f"Result: {fight.result.value}")  # "win" or "loss"
   print(f"Turns: {fight.turns}")

   # XP and gold earned
   for cr in fight.characters:
       print(f"+{cr.xp} XP, +{cr.gold} gold")

   # Drops (loot)
   for cr in fight.characters:
       if cr.drops:
           for drop in cr.drops:
               print(f"Drop: {drop.code} x{drop.quantity}")

   # Boss fight (with other players)
   result = char.fight(participants=["Player2", "Player3"])

Rest
^^^^

.. code-block:: python

   # Recover HP
   result = char.rest()
   print(f"+{result.hp_restored} HP")

Character Info
^^^^^^^^^^^^^^^

.. code-block:: python

   info = char.get()

   # General
   print(f"Name: {info.name}")
   print(f"Level: {info.level}")
   print(f"XP: {info.xp}/{info.max_xp}")
   print(f"Gold: {info.gold}")
   print(f"HP: {info.hp}/{info.max_hp}")

   # Position
   print(f"Position: ({info.x}, {info.y})")

   # Skills
   print(f"Mining: level {info.mining_level}")
   print(f"Woodcutting: level {info.woodcutting_level}")
   print(f"Fishing: level {info.fishing_level}")

   # Inventory
   for slot in info.inventory:
       print(f"  {slot.code} x{slot.quantity}")

Sub-Domains
-------------

Your character has **action groups** for each aspect of the game:

.. code-block:: text

   char.skills      → Gathering, crafting, recycling
   char.equipment   → Equip / unequip items
   char.bank        → Bank (gold and items)
   char.inventory   → Use / delete items
   char.ge          → Grand Exchange (marketplace)
   char.tasks       → Quests
   char.trading     → NPC and player-to-player trading

Each group has its own methods. They're covered in the following
pages!

Cooldowns
----------

Every action in Artifacts MMO triggers a **cooldown** (wait time).
By default, the SDK waits automatically before the next action.

.. code-block:: python

   char.move(x=0, y=1)   # waits for move cooldown
   char.fight()           # waits for fight cooldown
   char.fight()           # waits for previous fight cooldown
   # Everything is smooth, no time.sleep() needed!

If you want to **disable** automatic waiting:

.. code-block:: python

   # Globally (for all characters)
   client.auto_wait = False

   # For a specific character
   char = client.character("MyChar", auto_wait=False)

   # For a single action
   result = char.fight(wait=False)

.. tip::

   With ``auto_wait=False``, you'll have to manage cooldowns yourself
   using ``wait_for_cooldown()`` or by catching errors.

Other Actions
--------------

Claim Pending Items
^^^^^^^^^^^^^^^^^^^^

Items from achievements, GE orders, or events go to your pending
items. Claim them with:

.. code-block:: python

   # Check pending items first
   pending = client.my_account.get_pending_items()
   for item in pending.data:
       print(f"Pending: {item.code} x{item.quantity}")

   # Claim by ID
   result = char.claim_item(id=12345)
   print("Item claimed!")

Change Skin
^^^^^^^^^^^^

.. code-block:: python

   from artifacts.models.enums import CharacterSkin

   char.change_skin(skin=CharacterSkin.WOMEN2)

Action History
---------------

.. code-block:: python

   logs = char.get_logs(page=1, size=10)
   for log in logs.data:
       print(f"{log.type.value} — {log.created_at}")

Next Step
---------

Head to :doc:`inventory` to manage items, then :doc:`skills` for gathering and crafting.
