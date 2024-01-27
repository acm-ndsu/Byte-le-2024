==============
The Game Board
==============

.. raw:: html

    <style> .red {color:#BC0C25; font-weight:bold; font-size:16px} </style>
    <style> .blue {color:#1769BC; font-weight:bold; font-size:16px} </style>
    <style> .green {color:#469B34; font-weight:bold; font-size:16px} </style>
    <style> .brown {color:#623514; font-weight:bold; font-size:16px} </style>
    <style> .gold {color:#E1C564; font-weight:bold; font-size:16px} </style>

.. role:: red
.. role:: blue
.. role:: green
.. role:: brown
.. role:: gold


Layout
======

The map is a 14x14 grid, including the outer walls. Both MOB-BOTs for either team will be on the same map.
The only thing separating them is the walls of The Quarry. However, if the two MOB-BOTs meet, it could be an explosive
battle!

:gold:`NOTE: Two MOB-BOTs cannot stand on the same tile. However, MOB-BOT can stand on Traps, Dynamite, and Ores.`

.. image:: ./_static/images/game_map.png
   :width: 50%
   :align: center


Tiles
=====

Coordinates
-----------

The map is made of a 2D array of Tile objects. To access any tiles, use (y, x) coordinates like so:

.. code-block:: python

   world.game_map[y][x]

For example, looking at the game map, there is Copium ore close to the :blue:`Church base` at coordinate (2, 1)
(remember that the top left is (0, 0)). To access that tile, type the following:

.. code-block:: python

   world.game_map[1][2]

Typing this will return the Tile object that has the ore at the specified coordinate.

Occupied_by
-----------

Each Tile object -- along with some others -- has an attribute called ``occupied_by``. This attribute allows for each Tile
to act like a stack to see everything that is on top of it.

For example, assume a Tile object has an OreOccupiableStation (an object that gives you ores when you mine), Dynamite,
and a MOB-BOT on it in that order. To see the first object the Tile is occupied by, type the following:

.. code-block:: python

   ore_occupiable_station = tile.occupied_by

Since the OreOccupiableStation is the first object in the stack, it will be the returned.

To check if the returned OreOccupiableStation is occupied by something, there are two ways to check this:

.. code-block:: python

   dynamite = ore_occupiable_station.occupied_by
   dynamite = tile.occupied_by.occupied_by

Both of these would return a Dynamite object in this example. For every object that is on a Tile, you can either use
an object reference and call ``occupied_by`` if it has it, or you can chain call ``occupied_by`` on the initial Tile
object.

To access the MOB-BOT from the tile, you can do the following:

.. code-block:: python

   avatar = dynamite.occupied_by
   dynamite = tile.occupied_by.occupied_by.occupied_by


Is_occupied_by and get_occupied_by
----------------------------------

If you simply want to check if a Tile is occupied by a certain object, you can type the following:

.. code-block:: python

   tile.is_occupied_by_object_type(ObjectType.EXAMPLE_OBJECT_TYPE)

The method will return a boolean representing if the Tile is occupied by the given enum. The method will only take an
ObjectType enum.

Lastly, to receive an object that is on a Tile, type:

.. code-block:: python

   tile.get_occupied_by(ObjectType.EXAMPLE_OBJECT_TYPE)

This method will take an ObjectType enum and search for it. If found, it will return the object. Otherwise, the ``None``
value will be returned.

The :doc:`placeables` page will explain everything that can be placed on the map by MOB-BOT, and :doc:`enums` will have
the enums needed for every object that can be on the game map.


Bases
-----

Each team will have a base on the map. Their base will match their MOB-BOT and company color.

- :blue:`Church Inc`.
    - :blue:`Church Inc.` will have the blue base in the top left corner.
- :red:`Turing Co.`
    - :red:`Turing Co.` will have the red base in the bottom right corner.

When you want to cash in ores for points or upgrade your MOB-BOT, you can only do so at your base. Once MOB-BOT is
standing on their base at the end of the turn, it will automatically deposit all the ores in its inventory.

More information on ores is found in :doc:`ores`, and information on MOB-BOT is found in :doc:`mobbot`.

Mining Interactions
===================

After mining ore from a Tile, there is a chance a new piece of ore is discovered underneath! Here's what can appear
after mining specific ores:

===================== ==========================================
Mined Ore             Next Generated Ore
===================== ==========================================
:green:`Copium`       :blue:`Lambdium` | :red:`Turite` | :brown:`Ancient Tech` | Nothing
:blue:`Lambdium`      :brown:`Ancient Tech` | Nothing
:red:`Turite`         :brown:`Ancient Tech` | Nothing
:brown:`Ancient Tech` Nothing
===================== ==========================================

Visit :doc:`ores` for more information on ore values.
