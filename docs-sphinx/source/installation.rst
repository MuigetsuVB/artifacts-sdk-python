Installation
============

Requirements
------------

- **Python 3.10** or newer
- An **Artifacts MMO account** (free at https://artifactsmmo.com)
- An **API token** (we'll show you how to get one below)

Install the SDK
----------------

.. code-block:: bash

   pip install artifacts-mmo

That's it! The SDK automatically installs its dependencies (``aiohttp``
and ``pydantic``).

Get Your Token
---------------

1. Go to https://artifactsmmo.com and log in
2. In your profile, generate an **API token** (JWT)
3. Copy the token — you'll need it in your code

.. warning::

   **Never** share your token with anyone!
   It's like a password for your characters.

You can also generate a token via code:

.. code-block:: python

   from artifacts import AsyncArtifactsClient
   import asyncio

   async def get_token():
       async with AsyncArtifactsClient() as client:
           token_info = await client.token.generate("username", "password")
           print(token_info.token)

   asyncio.run(get_token())

Verify Everything Works
------------------------

Run this mini-script to check:

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       status = client.server.get_status()
       print(f"Server v{status.version}")
       print(f"{status.characters_online} players online")

If you see ``Server v...`` printed, you're good to go!

Next Step
---------

Head to :doc:`getting-started`.
