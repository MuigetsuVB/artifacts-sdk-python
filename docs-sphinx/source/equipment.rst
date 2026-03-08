Equipment
=========

Equip your character with weapons, armor, and accessories to
make them stronger in combat.

Equip an Item
--------------

.. code-block:: python

   from artifacts.models.enums import ItemSlot

   # Equip a sword
   char.equipment.equip(code="iron_sword", slot=ItemSlot.WEAPON)

   # Equip a helmet
   char.equipment.equip(code="iron_helmet", slot=ItemSlot.HELMET)

   # Equip a ring
   char.equipment.equip(code="copper_ring", slot=ItemSlot.RING1)

Unequip an Item
----------------

.. code-block:: python

   # Remove weapon
   char.equipment.unequip(slot=ItemSlot.WEAPON)

   # Remove a ring
   char.equipment.unequip(slot=ItemSlot.RING1)

Slots
------

+-------------------+---------------------------------------+
| Slot              | Description                           |
+===================+=======================================+
| ``WEAPON``        | Main weapon                           |
+-------------------+---------------------------------------+
| ``SHIELD``        | Shield                                |
+-------------------+---------------------------------------+
| ``HELMET``        | Helmet                                |
+-------------------+---------------------------------------+
| ``BODY_ARMOR``    | Chestplate                            |
+-------------------+---------------------------------------+
| ``LEG_ARMOR``     | Leggings                              |
+-------------------+---------------------------------------+
| ``BOOTS``         | Boots                                 |
+-------------------+---------------------------------------+
| ``RING1``         | First ring                            |
+-------------------+---------------------------------------+
| ``RING2``         | Second ring                           |
+-------------------+---------------------------------------+
| ``AMULET``        | Amulet                                |
+-------------------+---------------------------------------+
| ``ARTIFACT1-3``   | Artifacts (3 slots)                   |
+-------------------+---------------------------------------+
| ``UTILITY1-2``    | Utility (consumables, etc.)           |
+-------------------+---------------------------------------+
| ``BAG``           | Bag (increases inventory)             |
+-------------------+---------------------------------------+
| ``RUNE``          | Rune                                  |
+-------------------+---------------------------------------+

View Current Equipment
-----------------------

.. code-block:: python

   info = char.get()

   print(f"Weapon: {info.weapon_slot}")
   print(f"Helmet: {info.helmet_slot}")
   print(f"Chest: {info.body_armor_slot}")
   print(f"Boots: {info.boots_slot}")
   print(f"Shield: {info.shield_slot}")
   print(f"Ring 1: {info.ring1_slot}")
   print(f"Ring 2: {info.ring2_slot}")
   print(f"Amulet: {info.amulet_slot}")

Browse Equipment in the Game
-----------------------------

.. code-block:: python

   # All weapons level 1-10
   weapons = client.items.get_all(type="weapon", min_level=1, max_level=10)
   for w in weapons.data:
       print(f"{w.name} (lvl {w.level})")
       for effect in w.effects:
           print(f"  {effect.name}: {effect.value}")

   # All body armor
   armor = client.items.get_all(type="body_armor", min_level=1, max_level=10)
   for a in armor.data:
       print(f"{a.name} (lvl {a.level})")

Next Step
---------

Head to :doc:`bank` to store your items safely.
