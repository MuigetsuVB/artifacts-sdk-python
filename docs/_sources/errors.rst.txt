Error Handling
===============

Errors happen! The SDK provides clear exceptions for every situation.
Here's how to handle them.

The Base Error
---------------

All SDK errors inherit from ``ArtifactsError``:

.. code-block:: python

   from artifacts.errors import ArtifactsError

   try:
       char.fight()
   except ArtifactsError as e:
       print(f"Error: {e}")

Most Common Errors
-------------------

Cooldown Active
^^^^^^^^^^^^^^^^

.. code-block:: python

   from artifacts.errors import CooldownActiveError

   try:
       char.fight(wait=False)  # without auto-wait
   except CooldownActiveError as e:
       print(f"Cooldown active! Code {e.code}")

.. tip::

   With ``auto_wait=True`` (the default), you'll **never** see
   this error — the SDK waits automatically.

Inventory Full
^^^^^^^^^^^^^^^

.. code-block:: python

   from artifacts.errors import InventoryFullError

   try:
       char.skills.gather()
   except InventoryFullError:
       print("Inventory full! Go deposit at the bank.")
       char.move(x=4, y=1)
       char.bank.deposit_items(items=[...])

Not Enough Gold
^^^^^^^^^^^^^^^^

.. code-block:: python

   from artifacts.errors import InsufficientGoldError

   try:
       char.trading.npc_buy(code="healing_potion", quantity=100)
   except InsufficientGoldError:
       print("Not enough gold!")

No Monster / Resource on Tile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from artifacts.errors import ContentNotOnMapError

   try:
       char.fight()
   except ContentNotOnMapError:
       print("Nothing to fight here.")

Error Reference Table
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 8 62

   * - Exception
     - Code
     - When it happens
   * - ``CooldownActiveError``
     - 499
     - Action too fast (cooldown not finished)
   * - ``ActionInProgressError``
     - 486
     - An action is already running
   * - ``InventoryFullError``
     - 497
     - No room left in inventory
   * - ``InsufficientGoldError``
     - 492
     - Not enough gold
   * - ``ContentNotOnMapError``
     - 598
     - Nothing to fight/gather on this tile
   * - ``AlreadyAtDestinationError``
     - 490
     - You're already on that tile
   * - ``SkillLevelTooLowError``
     - 493
     - Skill level too low
   * - ``CharacterNotFoundError``
     - 498
     - Character not found
   * - ``EquipmentSlotError``
     - 491
     - Equipment slot problem
   * - ``MapBlockedError``
     - 596
     - Tile is blocked
   * - ``NoPathError``
     - 595
     - No path to destination
   * - ``ConditionsNotMetError``
     - 496
     - Conditions not met
   * - ``TaskError``
     - 474+
     - Quest-related error
   * - ``GrandExchangeError``
     - 433+
     - Grand Exchange error
   * - ``RetryExhaustedError``
     - n/a
     - Too many failed attempts

Handling Errors Cleanly
------------------------

.. code-block:: python

   from artifacts.errors import (
       ContentNotOnMapError,
       InventoryFullError,
       ArtifactsError,
   )

   def farm_combat(char, num_fights=10):
       for i in range(num_fights):
           try:
               result = char.fight()
               print(f"Fight {i+1}: {result.fight.result.value}")
           except ContentNotOnMapError:
               print("No monster here!")
               break
           except InventoryFullError:
               print("Inventory full, depositing at bank...")
               # deposit logic here...
               break
           except ArtifactsError as e:
               print(f"Unexpected error: {e}")
               break

Automatic Retry
----------------

The SDK automatically retries requests on network errors or rate
limits (429). You can configure the retry behavior:

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.http import RetryConfig

   with ArtifactsClient(
       token="your_token",
       retry=RetryConfig(
           max_retries=5,           # 5 attempts max
           base_delay=1.0,          # 1 second before first retry
           max_delay=30.0,          # max 30 seconds wait
           retry_on_cooldown=True,  # retry on cooldown errors
       ),
   ) as client:
       char = client.character("MyChar")
       char.fight()
