Account & Characters
=====================

Manage your account and characters through the SDK.

Account Info
-------------

.. code-block:: python

   # Your account details
   details = client.my_account.get_details()
   print(f"Username: {details.username}")
   print(f"Status: {details.status.value}")

   # Your bank overview
   bank = client.my_account.get_bank()
   print(f"Gold: {bank.gold}")
   print(f"Slots: {bank.slots}")
   print(f"Expansions: {bank.expansions}")

   # All account logs
   logs = client.my_account.get_all_logs(page=1, size=20)
   for log in logs.data:
       print(f"{log.type.value} — {log.created_at}")

   # Change password
   client.my_account.change_password("old_password", "new_password")

Pending Items
--------------

Items from achievements, Grand Exchange buys, or admin gifts end up
in your **pending items**. Claim them with your character.

.. code-block:: python

   # Check pending items
   pending = client.my_account.get_pending_items()
   for item in pending.data:
       print(f"{item.code} x{item.quantity} (from: {item.source.value})")

   # Claim them with a character
   char = client.character("MyChar")
   for item in pending.data:
       result = char.claim_item(item.id)
       print(f"Claimed {item.code}!")

GE History
-----------

.. code-block:: python

   # Your Grand Exchange transaction history
   history = client.my_account.get_ge_history()
   for h in history.data:
       print(f"{h.code} x{h.quantity} @ {h.price}g")

Character Management
---------------------

Create Characters
^^^^^^^^^^^^^^^^^^

You can have up to **5 characters** per account.

.. code-block:: python

   from artifacts.models.enums import CharacterSkin

   # Create a new character
   new_char = client.characters.create("MyNewChar", CharacterSkin.MEN1)
   print(f"Created {new_char.name} (level {new_char.level})")

Available skins: ``MEN1``, ``MEN2``, ``MEN3``, ``WOMEN1``, ``WOMEN2``,
``WOMEN3``, and special skins like ``ZOMBIE1``, ``GOBLIN1``.

Delete Characters
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Delete a character (permanent!)
   deleted = client.characters.delete("OldChar")
   print(f"Deleted {deleted.name}")

.. warning::

   Character deletion is **permanent**. All items, gold, and progress
   on that character will be lost.

Change Skin
^^^^^^^^^^^^^

.. code-block:: python

   from artifacts.models.enums import CharacterSkin

   char = client.character("MyChar")
   char.change_skin(skin=CharacterSkin.WOMEN2)

View Other Players
-------------------

.. code-block:: python

   # Look up another player's account
   account = client.accounts.get("SomePlayer")
   print(f"{account.username} — status: {account.status.value}")

   # Their characters
   chars = client.accounts.get_characters("SomePlayer")
   for c in chars.data:
       print(f"  {c.name} lv{c.level}")

   # Their achievements
   achievements = client.accounts.get_achievements("SomePlayer")
   for a in achievements.data:
       print(f"  {a.code}")

   # See who's currently online
   active = client.characters.get_active()
   for c in active.data:
       print(f"{c.name} ({c.account}) at ({c.x},{c.y})")

Account Creation
-----------------

.. code-block:: python

   # Create a new account
   client.accounts.create(
       username="new_player",
       password="secure_password",
       email="player@example.com",
   )

   # Forgot password
   client.accounts.forgot_password(email="player@example.com")

   # Reset password (with token from email)
   client.accounts.reset_password(token="reset_token", new_password="new_pass")
