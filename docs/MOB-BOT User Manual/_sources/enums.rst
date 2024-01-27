=====
Enums
=====

.. raw:: html

    <style> .gold {color:#E1C564; font-weight:bold; font-size:16px} </style>

.. role:: gold

The use of enums will manage which actions you'd like to do. Pass these in to control your MOB-BOT! Make sure to type
``from game.common.enums import *`` to have access to all the enums you'll need.


Company Enums
=============

============== =========
Enum Name      Int Value
============== =========
Company.CHURCH 1
Company.TURING 2
============== =========


ObjectType Enums
================

Ores
----

======================= =========
Enum Name               Int Value
======================= =========
ObjectType.LAMBDIUM     11
ObjectType.TURITE       12
ObjectType.COPIUM       13
ObjectType.ANCIENT_TECH 15
======================= =========


Stations
--------
================================= =========
Enum Name                         Int Value
================================= =========
ObjectType.CHURCH_STATION         22
ObjectType.TURING_STATION         23
ObjectType.ORE_OCCUPIABLE_STATION 30
================================= =========


Placeables
----------
=================== =========
Enum Name           Int Value
=================== =========
ObjectType.DYNAMITE 29
ObjectType.LANDMINE 32
ObjectType.EMP      33
=================== =========


Other
-----

:gold:`NOTE: ObjectType.AVATAR refers to the ObjectType of your MOB-BOT!`

================================= =========
Enum Name                         Int Value
================================= =========
ObjectType.AVATAR                 4
ObjectType.GAMEBOARD              5
ObjectType.VECTOR                 6
ObjectType.TILE                   7
ObjectType.WALL                   8
================================= =========


ActionType Enums
================

Movement
--------

===================== =========
Enum Name             Int Value
===================== =========
ActionType.MOVE_UP    2
ActionType.MOVE_DOWN  3
ActionType.MOVE_LEFT  4
ActionType.MOVE_RIGHT 5
===================== =========


Placing
-------

========================= =========
Enum Name                 Int Value
========================= =========
ActionType.PLACE_DYNAMITE 11
ActionType.PLACE_LANDMINE 12
ActionType.PLACE_EMP      13
========================= =========


Mining
------
=============== =========
Enum Name       Int Value
=============== =========
ActionType.MINE 14
=============== =========


Defusing Traps
--------------

================= =========
Enum Name         Int Value
================= =========
ActionType.DEFUSE 15
================= =========


Buying New Techs
----------------

====================================  =========
Enum Name                             Int Value
====================================  =========
ActionType.BUY_IMPROVED_DRIVETRAIN    16
ActionType.BUY_SUPERIOR_DRIVETRAIN    17
ActionType.BUY_OVERDRIVE_DRIVETRAIN   18
ActionType.BUY_IMPROVED_MINING        19
ActionType.BUY_SUPERIOR_MINING        20
ActionType.BUY_OVERDRIVE_MINING       21
ActionType.BUY_DYNAMITE               22
ActionType.LANDMINES                  23
ActionType.BUY_EMPS                   24
ActionType.BUY_TRAP_DEFUSAL           25
====================================  =========
