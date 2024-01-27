===============
Useful Commands
===============

.. raw:: html

    <style> .red {color:#BC0C25; font-weight:bold; font-size:16px} </style>

.. role:: red

Running the launcher
====================

There are required packages necessary for running the game. Run the following command to install them all:

.. code-block:: console

    pip install -r requirements.txt

You can view the list of packages in the requirements.txt file.


Pygame Installation
===================

If you have problems installing the pygame package, try running the following command:

.. code-block:: console

    pip install pygame --pre


Generate, Run, Visualize!
=========================

As you're testing, it's important to do these three actions. 'Generate' will generate a new game and map.
'Run' will execute the most recently generated game. 'Visualize' will visualize what happened in the last ran game.

Here are the commands:

Generate
--------

Run the following in the root directory in your terminal:

.. code-block::

    python launcher.pyz g

If you don't want to have a new, random seed, don't run this command. With the same seed and clients, the results will
stay consistent.


Run
---

.. code-block::

    python launcher.pyz r

As the game is running, any print statements you have will print to your console, which can be useful for
debugging. There will also be logs generated in the ``logs`` folder, showing what information was stored each turn in
the JSON format.

Visualize
----------

.. code-block::

    python launcher.pyz v

This will visualize the game you ran, allowing you to debug in a more user-friendly way! How wonderful.

Visit :doc:`visualizer` to get a better understanding of how it works.


Quality of Life!
================

Generate, Run, and Visualize all at Once!
-----------------------------------------
It would be annoying if you wanted to generate, run, and visualize using three separate commands, so we condensed
them for you!

If you type

.. code-block::

    python launcher.pyz grv

in the terminal, it will generate, run, and visualize all at once in one command! How nice.


Generate and Run
----------------

"What if I don't want to visualize, but only generate and run?" We've got you covered!

.. code-block::

    python launcher.pyz gr

This command will generate and run your game without using the visualizer. How convenient.


Terminal Help
-------------

Lastly, a list of commands will be listed by typing

.. code-block::

    python launcher.pyz -h

in the terminal. Each of the sub-commands will have their own help messages too.

|

.. figure:: ./_static/images/turing_comp.png

(:red:`Turing Inc.` MOB-BOT using terminal commands to visualize The Quarry)

