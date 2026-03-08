Events
======

Events are **limited-time spawns** that appear on the map. They can
be special monsters, resources, or other content that's only available
for a short period.

View Active Events
-------------------

.. code-block:: python

   # See what's happening right now
   active = client.events.get_all_active()
   for event in active.data:
       print(f"{event.code} at ({event.x},{event.y}) — expires {event.expiration}")

Browse All Events
------------------

.. code-block:: python

   # See all event definitions (including past ones)
   events = client.events.get_all()
   for event in events.data:
       print(f"{event.code} — {event.name}")

Spawn an Event (Members Only)
-------------------------------

Members (founders) can **spawn events** manually:

.. code-block:: python

   # Spawn an event by code
   event = client.events.spawn("special_boss")
   print(f"Spawned {event.code} at ({event.x},{event.y})!")

.. warning::

   ``events.spawn()`` requires a **member/founder** account. Free
   accounts can only view active events.

Fighting Event Monsters
------------------------

Once an event is active, move your character to its tile and fight:

.. code-block:: python

   # Check active events
   active = client.events.get_all_active()
   if active.data:
       event = active.data[0]
       print(f"Event: {event.code} at ({event.x},{event.y})")

       # Move there and fight
       char.move(x=event.x, y=event.y)
       result = char.fight()
       print(f"Result: {result.fight.result.value}")
