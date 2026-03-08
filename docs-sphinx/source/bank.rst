Bank
====

The bank lets you store gold and items safely.
Your character must be **on a bank tile** to perform operations.

.. tip::

   Find banks with:

   .. code-block:: python

      banks = client.maps.get_all(content_type="bank")
      for b in banks.data:
          print(f"Bank at ({b.x}, {b.y})")

Deposit and Withdraw Gold
--------------------------

.. code-block:: python

   # Go to the bank
   char.move(x=4, y=1)

   # Deposit 500 gold
   char.bank.deposit_gold(quantity=500)

   # Withdraw 200 gold
   char.bank.withdraw_gold(quantity=200)

Deposit and Withdraw Items
---------------------------

.. code-block:: python

   from artifacts.models.common import SimpleItemSchema

   # Deposit items
   char.bank.deposit_items(items=[
       SimpleItemSchema(code="iron_ore", quantity=50),
       SimpleItemSchema(code="copper_ore", quantity=30),
   ])

   # Withdraw items
   char.bank.withdraw_items(items=[
       SimpleItemSchema(code="iron_ore", quantity=10),
   ])

Expand the Bank
----------------

If you're running out of space, you can buy an expansion:

.. code-block:: python

   char.bank.buy_expansion()

Check Bank Contents
--------------------

.. code-block:: python

   # Items in bank
   bank_items = client.my_account.get_bank_items()
   for item in bank_items.data:
       print(f"{item.code} x{item.quantity}")

   # Bank overview (gold + slot info)
   bank = client.my_account.get_bank()
   print(f"Gold in bank: {bank.gold}")
   print(f"Slots: {bank.slots}")
   print(f"Expansions: {bank.expansions}")

   # Search for a specific item in bank
   iron = client.my_account.get_bank_items(item_code="iron_ore")
   for item in iron.data:
       print(f"{item.code} x{item.quantity}")

Next Step
---------

Head to :doc:`grand-exchange` to sell and buy on the Grand Exchange.
