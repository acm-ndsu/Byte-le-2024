===============
Getting Started
===============

.. raw:: html

    <style> .red {color:#BC0C25; font-weight:bold; font-size:16px} </style>
    <style> .blue {color:#1769BC; font-weight:bold; font-size:16px} </style>
    <style> .gold {color:#E1C564; font-weight:bold; font-size:16px} </style>

.. role:: red
.. role:: blue
.. role:: gold


NOTICE
======

Please run the following command to install the necessary packages to run the game:

.. code-block:: console

    python -m pip install -r requirements.txt

More commands are listed in :doc:`useful_commands`. Thank you!


Objective
=========
Your objective for this year is to gain more points than your opponents. This is done by mining more ores than the
opposing team in The Quarry, and by unlocking upgrades. :doc:`scoring` will explain how the points are totaled. Each
game will have 500 turns before ending. Manage your time wisely!

As you collect ores, make your way back to your base to cash them in for game points and science points!
Upgrading your MOB-BOT with science points will increase its mining capabilities, thus improving corporate revenue
(fantastic)! You can even disrupt the opposing team with traps, giving you the advantage and removing the competition
from the market (astounding)!

Visit :doc:`mobbot` for more information on how it all works.

Remember -- failure to comply with the high standards of the company, along with failure to defeat the rival
company in the task of mining the most ore, will result in ``immediate termination``. But you'll be okay.
``:)``


Tournament Structure
====================
Each pairing of teams will have two games against each other. After one game, both teams will switch company
affiliations (i.e., if first with :blue:`Church Inc.`, will next be :red:`Turing Co.`). The points gained from both
games will be added to those teams' total points in the tournament.


Running the Game
================
Python Version
--------------

Make sure to uninstall the visual studio version of python if you have visual studio installed.
You can do this by re-running the installer and unselecting the python development kit then clicking update.

:gold:`We require using Python version 3.11.` You can go to the
`official Python website <https://www.python.org/downloads/release/python-3117/>`_ to download it.

You can use any text editor or IDE for this competition, but we recommend Visual Studio Code.


Getting the Code and MOB-BOT
----------------------------

To receive the code and your own MOB-BOT, please clone the repository here
`here <https://github.com/acm-ndsu/Byte-le-2024>`_.

When on GitHub, press the green ``<> Code`` button to drop down the following menu:

.. image:: ./_static/images/clone_repo_options.png

We highly recommend cloning with GitHub Desktop or downloading the ZIP folder.

#. Open with GitHub Desktop
    * Allow the website to open GitHub Desktop if you have it downloaded already
    * Once in GitHub Desktop, the URL to the repository will be provided
    * Choose where you'd like it saved on your device
    * Click ``Clone`` and you're good to go!

    .. image:: ./_static/images/github_desktop_cloning.png

#. Download ZIP
    * Click ``Download ZIP`` and find it in your Downloads.
    * Extract the files and save it some where on your device.
    * Use your IDE/text editor (Visual Studio Code is recommended) of choice and open the extracted folder downloaded.
    * You're ready to code!


Submitting Code
---------------

To submit your code, program MOB-BOT in either your ``base_client.py`` or ``base_client_2.py`` files. When you submit
your code via the command specified in :doc:`server`, you can submit either of these files if you choose to.


Submitting Issues
-----------------

If you run into issues with the game, please submit an issue to the discord in the bugs channel or call a developer
over!
