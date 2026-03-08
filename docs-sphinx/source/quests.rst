Quests (Tasks)
===============

Quests give you **rewards** in exchange for killing monsters or
gathering items. Talk to a **Task Master** to get one.

.. code-block:: python

   # Find a task master
   task_masters = client.maps.get_all(content_type="tasks_master")
   for m in task_masters.data:
       print(f"Task master at ({m.x}, {m.y})")

Quest Lifecycle
----------------

.. code-block:: python

   # 1. Move to the task master
   char.move(x=1, y=2)

   # 2. Accept a new quest
   task = char.tasks.new()
   print(f"Quest: {task.task.type.value}")
   print(f"Target: {task.task.code}")
   print(f"Required: {task.task.total}")

   # 3. Complete the quest (fight or gather depending on type)
   # ... (see examples below)

   # 4. Go back to the task master
   char.move(x=1, y=2)

   # 5. Turn in the quest and claim the reward
   reward = char.tasks.complete()
   print("Reward claimed!")

Exchange Rewards
-----------------

After completing enough quests, you can **exchange** task tokens
for special rewards:

.. code-block:: python

   reward = char.tasks.exchange()

Deliver Items for a Quest
--------------------------

.. code-block:: python

   char.tasks.trade(code="iron_ore", quantity=10)

Cancel a Quest
---------------

.. code-block:: python

   char.tasks.cancel()

.. warning::

   Cancelling a quest may have a cost! Think before you cancel.

Full Example: Quest Loop
--------------------------

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       char = client.character("MyChar")

       for i in range(5):
           # Go to the task master
           char.move(x=1, y=2)

           # New quest
           task = char.tasks.new()
           code = task.task.code
           total = task.task.total
           print(f"Quest {i+1}: kill {total}x {code}")

           # Find where the monster spawns
           spots = client.maps.get_all(content_code=code, content_type="monster")
           if spots.data:
               spot = spots.data[0]
               char.move(x=spot.x, y=spot.y)

               for _ in range(total):
                   char.fight()

           # Go back and turn in
           char.move(x=1, y=2)
           char.tasks.complete()
           print(f"Quest {i+1} done!")

Next Step
---------

Head to :doc:`trading` for NPC and player-to-player trading.
