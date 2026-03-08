Grand Exchange
=============================

The Grand Exchange (GE) is the **player Grand Exchange**. You can sell
your items and buy from others.

Your character must be on a **Grand Exchange tile** to trade.

.. code-block:: python

   # Find the Grand Exchange
   ge_maps = client.maps.get_all(content_type="grand_exchange")
   for m in ge_maps.data:
       print(f"GE at ({m.x}, {m.y})")

Create a Sell Order
-------------

.. code-block:: python

   # Go to the GE
   char.move(x=5, y=1)

   # List 10 iron ore at 5 gold each
   char.ge.sell(code="iron_ore", quantity=10, price=5)

Buy an Item
------------

.. code-block:: python

   # Buy from an existing listing (by its ID)
   char.ge.buy(id=12345, quantity=5)

Create a Buy Order
-------------------

You can also create a **buy order** — other players can then fill it by selling items to you:

.. code-block:: python

   # Create a buy order
   char.ge.create_buy_order(code="iron_ore", quantity=50, price=4)

Fill a Buy Order
-----------------

You can sell your items directly to another player's active buy order:

.. code-block:: python

   # Fill an existing buy order (by its ID)
   char.ge.fill(id="some_order_id", quantity=10)

Cancel an Order
----------------

.. code-block:: python

   char.ge.cancel(id=12345)

Browse Orders
--------------

.. code-block:: python

   # See all orders for an item
   orders = client.grand_exchange.get_orders(code="iron_ore")
   for order in orders.data:
       print(f"[{order.type.value}] {order.code} x{order.quantity} @ {order.price}g")

   # Get a specific order by ID
   order = client.grand_exchange.get_order(12345)
   print(f"{order.code} x{order.quantity} @ {order.price}g")

   # My active orders
   my_orders = client.my_account.get_ge_orders()
   for order in my_orders.data:
       print(f"{order.code} x{order.quantity} @ {order.price}g ({order.type.value})")

Price History
--------------

.. code-block:: python

   # Price history for an item
   history = client.grand_exchange.get_history("iron_ore")
   for h in history.data:
       print(f"{h.code} x{h.quantity} @ {h.price}g")

   # Your personal GE history
   my_history = client.my_account.get_ge_history()
   for h in my_history.data:
       print(f"{h.code} x{h.quantity} @ {h.price}g")

Next Step
---------

Head to :doc:`tasks` to accept and complete tasks.
