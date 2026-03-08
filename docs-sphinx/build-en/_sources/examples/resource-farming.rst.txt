Resource Farming
=================

A bot that gathers resources, deposits them at the bank, and
optionally crafts items.

Gathering Loop
---------------

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.errors import InventoryFullError

   TOKEN = "your_token_here"

   with ArtifactsClient(token=TOKEN) as client:
       char = client.character("MyGatherer")

       # Find a mining spot
       mining_spots = client.maps.get_all(content_type="resource", size=20)
       for spot in mining_spots.data:
           print(f"Resource at ({spot.x},{spot.y}) — {spot.content.code}")

       # Go to first copper spot (adjust coordinates)
       SPOT_X, SPOT_Y = 2, 0
       char.move(x=SPOT_X, y=SPOT_Y)

       gathered = {}
       for i in range(20):
           try:
               result = char.skills.gather()
           except InventoryFullError:
               print("Inventory full! Going to bank...")
               break

           print(f"[{i+1}/20] +{result.xp} XP")
           for item in result.items:
               gathered[item.code] = gathered.get(item.code, 0) + item.quantity
               print(f"  {item.code} x{item.quantity}")

       print(f"\nTotal gathered: {gathered}")

Gather → Bank → Repeat
------------------------

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.errors import InventoryFullError
   from artifacts.models.common import SimpleItemSchema

   TOKEN = "your_token_here"
   RESOURCE_X, RESOURCE_Y = 2, 0   # mining spot
   BANK_X, BANK_Y = 4, 1           # bank location

   with ArtifactsClient(token=TOKEN) as client:
       char = client.character("MyGatherer")

       for cycle in range(5):
           print(f"\n=== Cycle {cycle+1} ===")

           # Go gather
           char.move(x=RESOURCE_X, y=RESOURCE_Y)
           bag = {}

           for _ in range(15):
               try:
                   result = char.skills.gather()
                   for item in result.items:
                       bag[item.code] = bag.get(item.code, 0) + item.quantity
               except InventoryFullError:
                   break

           print(f"Gathered: {bag}")

           # Go deposit at bank
           char.move(x=BANK_X, y=BANK_Y)
           items_to_deposit = [
               SimpleItemSchema(code=code, quantity=qty)
               for code, qty in bag.items()
           ]
           if items_to_deposit:
               char.bank.deposit_items(items=items_to_deposit)
               print("Deposited at bank!")

       print("\nAll cycles done!")

Gather → Craft → Sell
-----------------------

.. code-block:: python

   from artifacts import ArtifactsClient
   from artifacts.models.common import SimpleItemSchema

   TOKEN = "your_token_here"

   with ArtifactsClient(token=TOKEN) as client:
       char = client.character("MyCrafter")

       # Step 1: Gather copper ore at a mining spot
       char.move(x=2, y=0)
       for _ in range(10):
           char.skills.gather()
       print("Gathered copper ores!")

       # Step 2: Go to a workshop and craft copper rings
       char.move(x=1, y=3)
       result = char.skills.craft(code="copper_ring", quantity=3)
       print(f"Crafted! +{result.xp} XP")

       # Step 3: Sell on the Grand Exchange
       char.move(x=5, y=1)
       char.ge.sell(code="copper_ring", quantity=3, price=10)
       print("Listed on GE!")

Tips
-----

- Use ``client.items.get("item_code")`` to check recipes before crafting
- Higher gathering skill = more items per gather
- Deposit regularly to avoid losing items if something goes wrong
