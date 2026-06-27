Gems Shop
=========

The gems shop exposes purchasable skins, event spawns, subscriptions, and
custom designs.

Browse the Catalog
------------------

.. code-block:: python

   catalog = client.gems_shop.get_catalog()

   for skin in catalog.skins:
       print(f"{skin.code}: {skin.price} gems")

   for event in catalog.spawn_events:
       print(f"{event.code}: {event.price} gems")

Buy a Skin
----------

.. code-block:: python

   purchase = client.gems_shop.buy_skin("skin_code")
   print(f"Remaining gems: {purchase.gems}")

Spawn an Event
--------------

.. code-block:: python

   event = client.gems_shop.spawn_event("event_code")
   print(f"Spawned {event.code}")

Buy a Subscription
------------------

.. code-block:: python

   subscription = client.gems_shop.buy_subscription()
   print(subscription.member_expiration)

Buy a Custom Design
-------------------

.. code-block:: python

   design = client.gems_shop.buy_custom_design("design_code")
   print(f"{design.name}: {design.cost} gems")
