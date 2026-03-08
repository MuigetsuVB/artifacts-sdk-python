Sandbox (Testing)
==================

The sandbox server lets you **test your bots** without affecting
the real game. You can give yourself gold, items, XP, and spawn
events at will.

.. note::

   Sandbox endpoints only work on the **sandbox server**. Connect
   with ``base_url="https://sandbox.artifactsmmo.com"``:

   .. code-block:: python

      from artifacts import ArtifactsClient

      with ArtifactsClient(
          token="your_token",
          base_url="https://sandbox.artifactsmmo.com",
      ) as client:
          # Sandbox-only methods are now available
          pass

Give Gold
----------

.. code-block:: python

   result = client.sandbox.give_gold(character="MyChar", quantity=10000)
   print(f"Gold given! New balance: {result.character.gold}")

Give Items
-----------

.. code-block:: python

   result = client.sandbox.give_item(
       character="MyChar",
       code="iron_sword",
       quantity=5,
   )
   print("Items given!")

Give XP
--------

.. code-block:: python

   from artifacts.models.enums import XPType

   # Give combat XP
   result = client.sandbox.give_xp(
       character="MyChar",
       type=XPType.COMBAT,
       amount=5000,
   )

   # Give mining XP
   result = client.sandbox.give_xp(
       character="MyChar",
       type=XPType.MINING,
       amount=3000,
   )

Available XP types: ``COMBAT``, ``MINING``, ``WOODCUTTING``, ``FISHING``,
``WEAPONCRAFTING``, ``GEARCRAFTING``, ``JEWELRYCRAFTING``, ``COOKING``,
``ALCHEMY``.

Spawn Events
-------------

.. code-block:: python

   event = client.sandbox.spawn_event(code="special_boss")
   print(f"Event spawned at ({event.x},{event.y})!")

Reset Account
--------------

.. warning::

   This **deletes all your characters and progress** on the sandbox
   server. Use with caution!

.. code-block:: python

   result = client.sandbox.reset_account()
   print(f"Account reset: {result}")

Typical Testing Workflow
-------------------------

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.models.enums import CharacterSkin, XPType

   SANDBOX_URL = "https://sandbox.artifactsmmo.com"

   with ArtifactsClient(token="your_token", base_url=SANDBOX_URL) as client:
       # Create a test character
       new_char = client.characters.create("TestBot", CharacterSkin.MEN1)
       print(f"Created {new_char.name}")

       # Give it resources to test with
       client.sandbox.give_gold(character="TestBot", quantity=50000)
       client.sandbox.give_item(character="TestBot", code="iron_sword", quantity=1)
       client.sandbox.give_item(character="TestBot", code="iron_armor", quantity=1)
       client.sandbox.give_xp(character="TestBot", type=XPType.COMBAT, amount=10000)

       # Now test your bot logic
       char = client.character("TestBot")
       info = char.get()
       print(f"Level {info.level}, {info.gold} gold")

       # Test fighting
       char.move(x=0, y=1)
       result = char.fight()
       print(f"Fight: {result.fight.result.value}")

       # When done, reset everything
       # client.sandbox.reset_account()
