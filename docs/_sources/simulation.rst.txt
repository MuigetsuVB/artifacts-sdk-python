Combat Simulation
==================

The SDK includes a **combat simulator** that lets you test fight
outcomes *without actually fighting*. This is useful for planning
your equipment and strategy.

.. warning::

   The simulation API requires a **member/founder** account.

How It Works
-------------

You create "fake" characters with specific equipment, then simulate
fights against a monster. The simulator runs multiple iterations and
gives you win/loss statistics.

Basic Simulation
-----------------

.. code-block:: python

   from artifacts.models.combat import FakeCharacterSchema

   # Create a simulated character
   fake_char = FakeCharacterSchema(
       level=15,
       weapon_slot="iron_sword",
       helmet_slot="iron_helmet",
       body_armor_slot="iron_armor",
       boots_slot="iron_boots",
   )

   # Simulate 100 fights against a wolf
   result = client.simulation.fight(
       characters=[fake_char],
       monster="wolf",
       iterations=100,
   )

   print(f"Wins: {result.wins}/{result.wins + result.losses}")
   print(f"Win rate: {result.winrate:.1%}")

Testing Different Builds
-------------------------

.. code-block:: python

   from artifacts.models.combat import FakeCharacterSchema

   # Build A: Heavy armor
   tank_build = FakeCharacterSchema(
       level=20,
       weapon_slot="iron_sword",
       shield_slot="iron_shield",
       helmet_slot="iron_helmet",
       body_armor_slot="iron_armor",
       leg_armor_slot="iron_legs",
       boots_slot="iron_boots",
   )

   # Build B: Glass cannon
   dps_build = FakeCharacterSchema(
       level=20,
       weapon_slot="steel_sword",
       ring1_slot="copper_ring",
       ring2_slot="copper_ring",
       amulet_slot="copper_amulet",
   )

   # Test both against the same monster
   for name, build in [("Tank", tank_build), ("DPS", dps_build)]:
       result = client.simulation.fight(
           characters=[build],
           monster="ogre",
           iterations=200,
       )
       print(f"{name}: {result.winrate:.1%} winrate ({result.wins}W/{result.losses}L)")

Multi-Character Boss Simulation
---------------------------------

You can simulate boss fights with multiple characters:

.. code-block:: python

   from artifacts.models.combat import FakeCharacterSchema

   chars = [
       FakeCharacterSchema(level=25, weapon_slot="steel_sword", body_armor_slot="steel_armor"),
       FakeCharacterSchema(level=25, weapon_slot="steel_sword", body_armor_slot="steel_armor"),
       FakeCharacterSchema(level=25, weapon_slot="steel_sword", body_armor_slot="steel_armor"),
   ]

   result = client.simulation.fight(
       characters=chars,
       monster="dragon_boss",
       iterations=50,
   )

   print(f"Win rate: {result.winrate:.1%}")
   print(f"Results: {result.wins}W / {result.losses}L")

   # View individual fight details
   for i, fight in enumerate(result.results[:5]):
       print(f"  Fight {i+1}: {fight.result.value} in {fight.turns} turns")

FakeCharacterSchema Slots
---------------------------

When building a fake character, you can set any equipment slot:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Parameter
     - Description
   * - ``level``
     - Character level (required)
   * - ``weapon_slot``
     - Weapon item code
   * - ``shield_slot``
     - Shield item code
   * - ``helmet_slot``
     - Helmet item code
   * - ``body_armor_slot``
     - Chestplate item code
   * - ``leg_armor_slot``
     - Leggings item code
   * - ``boots_slot``
     - Boots item code
   * - ``ring1_slot``
     - First ring item code
   * - ``ring2_slot``
     - Second ring item code
   * - ``amulet_slot``
     - Amulet item code
   * - ``artifact1_slot``
     - Artifact slot 1
   * - ``artifact2_slot``
     - Artifact slot 2
   * - ``artifact3_slot``
     - Artifact slot 3
   * - ``rune_slot``
     - Rune item code
   * - ``utility1_slot``
     - Utility item 1
   * - ``utility2_slot``
     - Utility item 2

All slot parameters are optional — just set the ones you want to test.

.. tip::

   Use ``client.items.get("item_code")`` to verify an item exists and
   check its stats before simulating.
