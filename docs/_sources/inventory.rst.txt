Inventory
=========

Manage the items in your character's inventory — use consumables
and delete unwanted items.

Use an Item
------------

Consumables (food, potions) can be used from the inventory:

.. code-block:: python

   # Use a healing item
   result = char.inventory.use(code="cooked_chicken", quantity=1)
   print("Used cooked chicken!")

   # Use multiple at once
   result = char.inventory.use(code="healing_potion", quantity=3)

Delete an Item
---------------

Remove items you don't need from your inventory:

.. code-block:: python

   # Delete junk items
   result = char.inventory.delete(code="feather", quantity=10)
   print("Deleted 10 feathers")

View Inventory
---------------

.. code-block:: python

   info = char.get()

   print(f"Inventory: {len(info.inventory)}/{info.inventory_max_items} slots")
   for slot in info.inventory:
       print(f"  {slot.code} x{slot.quantity}")

Tips
-----

- **Deposit before deleting**: Consider banking items instead of deleting
- **Use food before fights**: Cooked food restores HP
- **Watch your inventory space**: You'll get ``InventoryFullError`` when full
- **Expand with bags**: Equip a bag in the ``BAG`` slot for more space
