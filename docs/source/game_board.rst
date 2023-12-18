==============
The Game Board
==============

Layout
======

The map is a 14x14 grid, including the outer walls. Both MOB-BOTs for either team will be on the same map.
The only thing separating them is the walls of The Quarry. However, if the two MOB-BOTs meet in the center
of the map, anything can happen!

The map is made of a 2D array of Tile objects. To access any tiles, you will use (y, x) coordinates like so:

.. code-block:: python

   world.game_map[y][x]


----

Tiles
=====

Tile objects can have any other object on top of them. The :doc:`placeables` page will explain everything that
can be placed on the map by MOB-BOT.
