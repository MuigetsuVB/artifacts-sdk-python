Skills
======

Your character can **gather** resources, **craft** items, and
**recycle** things you no longer need.

All these actions go through ``char.skills``.

Gathering
---------

To gather, you need to be on a tile that contains a resource
(tree, rock, fishing spot, etc.).

.. code-block:: python

   # Move to a tree (example)
   char.move(x=2, y=0)

   # Gather
   result = char.skills.gather()

   print(f"+{result.xp} XP")
   for item in result.items:
       print(f"Gathered: {item.code} x{item.quantity}")

.. tip::

   To find gathering spots, use ``client.maps``:

   .. code-block:: python

      maps = client.maps.get_all(content_type="resource", size=20)
      for m in maps.data:
          print(f"({m.x},{m.y}) — {m.content.code}")

Crafting
--------

To craft, you need:

1. The right **materials** in your inventory
2. To be on the matching **workshop** tile

.. code-block:: python

   # Check an item's recipe
   item = client.items.get("copper_ring")
   if item.craft:
       print(f"Skill: {item.craft.skill.value}")
       print(f"Required level: {item.craft.level}")
       for mat in item.craft.items:
           print(f"  {mat.code} x{mat.quantity}")

   # Move to a jewelrycrafting workshop
   char.move(x=1, y=3)

   # Craft
   result = char.skills.craft(code="copper_ring", quantity=1)
   print(f"+{result.xp} XP")

.. note::

   Workshops are on the map. Use ``client.maps.get_all(content_type="workshop")``
   to find them.

Recycling
---------

You can recycle crafted items to get back some of the materials.
You need to be on the matching workshop tile.

.. code-block:: python

   result = char.skills.recycle(code="copper_ring", quantity=1)
   for item in result.items:
       print(f"Recovered: {item.code} x{item.quantity}")

Gathering Skills
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Skill
     - What it gathers
   * - Mining
     - Ores (copper, iron, gold...)
   * - Woodcutting
     - Wood (ash, birch, dead_tree...)
   * - Fishing
     - Fish (shrimp, trout, bass...)
   * - Alchemy
     - Plants and ingredients

Crafting Skills
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Skill
     - What it makes
   * - Weaponcrafting
     - Weapons (swords, daggers, staffs)
   * - Gearcrafting
     - Armor (helmets, chestplates, boots)
   * - Jewelrycrafting
     - Jewelry (rings, amulets)
   * - Cooking
     - Food (restores HP)
   * - Alchemy
     - Potions and consumables

Typical Farming Loop
---------------------

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       char = client.character("MyChar")

       # Go to the mining spot
       char.move(x=1, y=5)

       # Gather 10 times
       for i in range(10):
           result = char.skills.gather()
           print(f"[{i+1}/10] +{result.xp} XP")
           for item in result.items:
               print(f"  {item.code} x{item.quantity}")

       print("Farming done!")

Next Step
---------

Head to :doc:`equipment` to equip the items you crafted.
