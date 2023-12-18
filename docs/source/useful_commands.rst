===============
Useful Commands
===============

Running the launcher
--------------------

There are required packages necessary for running the game. Run the following command to install them all:

.. code-block:: console

    python -m pip install -r requirements.txt

You can view the list of packages in the requirements.txt file. We have nothing to hide.


----

Pygame Installation
-------------------

If you have problems installing the pygame package, try running the following command:

.. code-block:: console

    python -m pip install pygame --pre


----

Generate, Run, Visualize!
=========================

As your testing, it's important to do these three actions. 'Generate' will... well, generate a new game and map.
'Run' will execute the most recently generated game. 'Visualize' will visualize what happened in the last ran game.

Here are the commands:

Generate
--------

Run the following in the byte-le folder:

.. code-block::

    python launcher.pyz g

If you don't want to have a new map, don't run this command. With the same map and clients, the results will stay
consistent.


Run
---

.. code-block::

    python launcher.pyz r

As the game is running, any print statements you have will print to your console, which can be useful for
debugging. There will also be logs generated in the `logs` folder, showing what information was stored turn by
turn.

Visualize!
----------

.. code-block::

    python launcher.pyz v

This will visualize the game you ran, allowing you to debug in a more user-friendly way! Thank
``<INSERT COMPANY NAME HERE>`` for that.

To understand the visualizer more, visit (this page).


Quality of Life!
----------------

It would be annoying if you wanted to generate, run, and visualize using three separate commands, so we condensed
them for you!

If you type

.. code-block::

    python launcher.pyz grv

in the terminal, it will generate, run, and visualize all at once in one command! How nice.


----

'But what if I don't want to visualize, but only generate and run?' We've got you covered!

.. code-block::

    python launcher.pyz gr

This command will generate and run your game without using the visualizer. How convenient.


----

Lastly, a list of commands will be listed by typing

.. code-block::

    python launcher.pyz -h

in the terminal. Each of the sub-commands will have their own help messages too, of course.
