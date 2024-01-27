=============
Taking Action
=============

.. raw:: html

        <style> .gold {color:#E1C564; font-weight:bold; font-size:16px} </style>

.. role:: gold

To control your MOB-BOT, you will be using :doc:`enums` to determine which action(s) take place each turn.


Take Turn Method
================

The take turn method will be where you program your MOB-BOT. The ``actions`` variable passed in is a list of ActionType
:doc:`enums`. Set your action(s) by typing the following:

.. code-block::

    actions = [ActionType.EXAMPLE_ENUM,]

Make sure to keep the ``return actions`` at the end of the method or your actions won't be received!

NOTE: If you will only provide a single enum to the list, add the comma at the end.

Action Management
=================

There are key things to note about how MOB-BOT will behave each turn as you create your actions.

Movement
--------

If you desire for MOB-BOT to move, make sure that the first action in your ``actions`` list is an ActionType enum for
movement. Since it is possible to move multiple Tiles in one turn, if the first enum is for movement, the rest of the
list will be filtered to :gold:`only` movement enums. The list size will then be based on MOB-BOT's movement speed.

For example, if MOB-BOT unlocked the Superior Drivetrain Tech to increase its movement speed to 3, an ``actions`` list
of:

.. code-block::

    actions = [ActionType.MOVE_DOWN, ActionType.MOVE_DOWN, ActionType.MINE, ActionType.MOVE_RIGHT, ActionType.MOVE_RIGHT]


will be filtered to:

.. code-block::

    actions = [ActionType.MOVE_DOWN, ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]

Now MOB-BOT can only move the first 3 movement enums specified.


Non-movement Actions
--------------------

In your ``actions`` list, if the first ActionType enum is :gold:`not` a movement option, that will be the only action
taken for that turn. This includes placing dynamite or traps, mining, defusing traps, and buying new Techs. Recall that
selling ores is done automatically as long as MOB-BOT ends the turn on its company base.


Buying Techs
------------

Buying Techs is done by using the specific :doc:`enums` while MOB-BOT is on its base. Attempting to buy a Tech otherwise
won't work.


Defusing Traps
--------------

Defusing traps is done by using an enum to defuse in a range from MOB-BOT.
