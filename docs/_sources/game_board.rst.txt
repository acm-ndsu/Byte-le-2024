==============
The Game Board
==============

Layout
======

The map is a 14x14 grid, including the outer walls. Both MOB-BOTs for either team will be on the same map.
The only thing separating them is the walls of The Quarry. However, if the two MOB-BOTs meet, it could be an explosive
battle!

.. image:: ./_static/images/game_map.png
   :width: 50%
   :align: center

The map is made of a 2D array of Tile objects. To access any tiles, you will use (y, x) coordinates like so:

.. code-block:: python

   world.game_map[y][x]


Tiles
=====

Tile objects can have any other object on top of them. The :doc:`placeables` page will explain everything that
can be placed on the map by MOB-BOT.

Bases
-----

Each team will have a base on the map. Their base will match their MOB-BOT and company color.

- Church Inc.
    - Church Inc. will have the blue base in the top left corner.
- Turing Co.
    - Turing Co. will have the red base in the bottom left corner.

When you want to cash in ores for points or upgrade your MOB-BOT, you can only do so at your base.

More information on ores is found in :doc:`ores`, and information on MOB-BOT is found in :doc:`mobbot`.

Mining Interactions
===================

After mining ore from a Tile, there is a chance a new piece of ore is discovered underneath! Here's what can appear
after mining specific ores:

============ ==========================================
Mined Ore    Next Generated Ore
============ ==========================================
Copium       Lambdium | Turite | Ancient Tech | Nothing
Lambdium     Ancient Tech | Nothing
Turite       Ancient Tech | Nothing
Ancient Tech Nothing
============ ==========================================

Visit :doc:`ores` for more information on ore values.
