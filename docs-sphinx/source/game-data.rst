Game Data
=========

The SDK gives you full access to all public game data — monsters,
items, resources, maps, achievements, effects, and more. All of
these are available through ``client.*`` and don't require your
character to be anywhere specific.

Monsters
--------

.. code-block:: python

   # Get info on a specific monster
   chicken = client.monsters.get("chicken")
   print(f"{chicken.name} — Level {chicken.level} — HP {chicken.hp}")

   # Browse all monsters
   monsters = client.monsters.get_all(min_level=1, max_level=10, size=10)
   for m in monsters.data:
       print(f"{m.name} lv{m.level} HP={m.hp}")

   # Find monsters that drop a specific item
   monsters = client.monsters.get_all(drop="feather")
   for m in monsters.data:
       print(f"{m.name} drops feather")

Items
-----

.. code-block:: python

   # Get a specific item
   item = client.items.get("iron_sword")
   print(f"{item.name} — Level {item.level} — {item.type.value}")

   # Browse by type
   weapons = client.items.get_all(type="weapon", min_level=1, max_level=10)
   for w in weapons.data:
       print(f"{w.name} (lv{w.level})")

   # Search by craft skill
   cooking_items = client.items.get_all(craft_skill="cooking")
   for item in cooking_items.data:
       print(f"{item.name} — crafted with cooking lv{item.craft.level}")

   # Search by craft material
   copper_items = client.items.get_all(craft_material="copper")
   for item in copper_items.data:
       print(f"{item.name} uses copper")

Resources
---------

Resources are gathering nodes on the map (trees, rocks, fish, etc.).

.. code-block:: python

   # Get a specific resource
   copper_rocks = client.resources.get("copper_rocks")
   print(f"{copper_rocks.code} — {copper_rocks.skill.value} lv{copper_rocks.level}")

   # Browse all resources
   resources = client.resources.get_all(skill="mining")
   for r in resources.data:
       print(f"{r.code} — mining lv{r.level}")

   # Filter by level range
   resources = client.resources.get_all(min_level=1, max_level=10)
   for r in resources.data:
       print(f"{r.code} — {r.skill.value} lv{r.level}")

   # Find resources that drop a specific item
   resources = client.resources.get_all(drop="copper_ore")
   for r in resources.data:
       print(f"{r.code} drops copper_ore")

Maps
----

.. code-block:: python

   # Browse all tiles
   maps = client.maps.get_all(content_type="monster", size=10)
   for m in maps.data:
       print(f"({m.x},{m.y}) — {m.content.code}")

   # Filter by layer (overworld, underground, interior)
   underground = client.maps.get_layer("underground", size=10)
   for m in underground.data:
       print(f"({m.x},{m.y}) — {m.content.code if m.content else 'empty'}")

   # Get a specific tile
   tile = client.maps.get_by_position("overworld", 0, 1)
   print(f"Tile ({tile.x},{tile.y}): {tile.content.code if tile.content else 'empty'}")

   # Get by map ID
   tile = client.maps.get_by_id(42)

   # Find all workshops
   workshops = client.maps.get_all(content_type="workshop")
   for m in workshops.data:
       print(f"Workshop at ({m.x},{m.y}) — {m.content.code}")

   # Find all banks
   banks = client.maps.get_all(content_type="bank")
   for b in banks.data:
       print(f"Bank at ({b.x},{b.y})")

Achievements
-------------

.. code-block:: python

   # Browse all achievements
   achievements = client.achievements.get_all()
   for a in achievements.data:
       print(f"{a.code} — {a.name} ({a.type.value})")

   # Filter by type
   combat_achievements = client.achievements.get_all(type="combat_kill")
   for a in combat_achievements.data:
       print(f"{a.code}: {a.description}")

   # Get a specific achievement
   ach = client.achievements.get("kill_100_chickens")
   print(f"{ach.name} — {ach.description}")

Badges
------

.. code-block:: python

   # Browse all badges
   badges = client.badges.get_all()
   for b in badges.data:
       print(f"{b.code} — {b.description}")

   # Get a specific badge
   badge = client.badges.get("some_badge_code")
   print(f"{badge.code}")

Effects
-------

.. code-block:: python

   # Browse all effects
   effects = client.effects.get_all()
   for e in effects.data:
       print(f"{e.code} — {e.name} ({e.type.value})")

   # Get a specific effect
   effect = client.effects.get("fire_attack_boost")
   print(f"{effect.name}: {effect.description}")

NPCs
----

.. code-block:: python

   # Browse all NPCs
   npcs = client.npcs.get_all()
   for npc in npcs.data:
       print(f"{npc.name} ({npc.code}) — {npc.type.value}")

   # Get a specific NPC
   npc = client.npcs.get("merchant_1")
   print(f"{npc.name}")

   # See what items an NPC sells
   npc = client.npcs.get("merchant_1")
   for item in npc.items:
       print(f"{item.code} — buy: {item.buy_price}g / sell: {item.sell_price}g ({item.currency})")

   # Filter NPCs by currency
   gold_npcs = client.npcs.get_all(currency="gold")

   # Filter NPCs that trade a specific item
   npcs_with_item = client.npcs.get_all(item="copper_ore")

Tasks (Static Data)
--------------------

View available task definitions and rewards (not your active quest —
see :doc:`quests` for that).

.. code-block:: python

   # Browse all task definitions
   tasks = client.tasks.get_all()
   for t in tasks.data:
       print(f"{t.code} — {t.type.value} lv{t.level}")

   # Get a specific task
   task = client.tasks.get("kill_chickens")
   print(f"{task.code} — {task.type.value}")

   # Browse task rewards
   rewards = client.tasks.get_all_rewards()
   for r in rewards.data:
       print(f"{r.code}")

   # Get a specific reward
   reward = client.tasks.get_reward("basic_reward")

Leaderboard
------------

.. code-block:: python

   # Top characters by combat level
   top = client.leaderboard.get_characters(sort="combat", size=10)
   for c in top.data:
       print(f"#{c.position} {c.name} — lv{c.level}")

   # Top characters by a specific skill
   miners = client.leaderboard.get_characters(sort="mining", size=10)
   for c in miners.data:
       print(f"#{c.position} {c.name} — mining lv{c.level}")

   # Search by name
   result = client.leaderboard.get_characters(name="MyChar")

   # Top accounts
   accounts = client.leaderboard.get_accounts(sort="achievements_points", size=10)
   for a in accounts.data:
       print(f"#{a.position} {a.account}")

Pagination
-----------

All ``get_all`` methods return a ``DataPage`` object with pagination:

.. code-block:: python

   page = client.items.get_all(size=50, page=1)

   print(f"Total items: {page.total}")
   print(f"Page {page.page} of {page.pages}")
   print(f"Items on this page: {len(page.data)}")

   # Loop through all pages
   all_items = []
   current_page = 1
   while True:
       result = client.items.get_all(size=50, page=current_page)
       all_items.extend(result.data)
       if current_page >= result.pages:
           break
       current_page += 1

   print(f"Fetched {len(all_items)} items total")
