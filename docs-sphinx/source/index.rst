.. Artifacts MMO Python SDK — Player Documentation

======================================
Artifacts MMO — Python SDK
======================================

Welcome! This SDK lets you **control your characters** in
`Artifacts MMO <https://artifactsmmo.com>`_ straight from a
Python script. You don't need to be an expert — a few lines of code
are enough to fight, gather, craft, and trade.

.. code-block:: python

   from artifacts import ArtifactsClient

   with ArtifactsClient(token="your_token") as client:
       char = client.character("MyChar")
       char.move(x=0, y=1)       # move
       result = char.fight()      # fight!
       print(result.fight.result) # "win"

**Don't want to use async/await?** The code above is 100 % synchronous.
The SDK handles cooldowns automatically — you don't have to do anything.

.. note::

   Requires Python 3.10+. Install: ``pip install artifacts-mmo``


Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Player Guide

   installation
   getting-started
   character
   inventory
   skills
   equipment
   bank
   marketplace
   quests
   trading
   errors

.. toctree::
   :maxdepth: 2
   :caption: Game World

   game-data
   events
   account

.. toctree::
   :maxdepth: 2
   :caption: Advanced Features

   simulation
   sandbox

.. toctree::
   :maxdepth: 2
   :caption: Full Examples

   examples/first-bot
   examples/combat-loop
   examples/resource-farming
   examples/multi-characters

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   reference/client
   reference/character
   reference/domains
   reference/errors


Index
=====

* :ref:`genindex`
* :ref:`search`
