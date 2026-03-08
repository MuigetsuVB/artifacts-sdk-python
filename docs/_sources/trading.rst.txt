Trading
=======

You can buy and sell items from **NPC merchants**, or give gold
and items to other players.

NPC Trading
------------

To trade with an NPC, you need to be on its tile.

.. code-block:: python

   # Find NPCs
   npc_maps = client.maps.get_all(content_type="npc")
   for m in npc_maps.data:
       print(f"NPC at ({m.x}, {m.y}) — {m.content.code}")

Buy from an NPC
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Go to the NPC
   char.move(x=2, y=3)

   # Buy healing potions
   char.trading.npc_buy(code="healing_potion", quantity=5)

Sell to an NPC
^^^^^^^^^^^^^^^

.. code-block:: python

   char.trading.npc_sell(code="feather", quantity=20)

Give to Another Player
-----------------------

You can give gold or items to another character **on the same tile**.

Give Gold
^^^^^^^^^^

.. code-block:: python

   char.trading.give_gold(quantity=100, character="OtherPlayer")

Give Items
^^^^^^^^^^^

.. code-block:: python

   from artifacts.models.common import SimpleItemSchema

   char.trading.give_items(
       items=[
           SimpleItemSchema(code="iron_ore", quantity=10),
           SimpleItemSchema(code="copper_ore", quantity=5),
       ],
       character="OtherPlayer"
   )

.. note::

   Both characters must be **on the same tile** for gold or
   item transfers.

Browse Available NPCs
----------------------

.. code-block:: python

   npcs = client.npcs.get_all()
   for npc in npcs.data:
       print(f"{npc.name} ({npc.code}) — {npc.type.value}")

Next Step
---------

Head to :doc:`errors` to learn how to handle errors like a pro.
