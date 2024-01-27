==============
MOB-BOT Part 2
==============

.. raw:: html

   <style> .strike {text-decoration: line-through} </style>

.. role:: strike


MOB-BOT is so complex, that corporate :strike:`forced` asked for a new page to explain it in more detail. Here you go!


MOB-BOT Properties
==================

Attributes
----------
Your MOB-BOT will come with a list of attributes you can use to see the current status of the game! This includes:

======================= ==================================================
Attributes              Descriptions
======================= ==================================================
mobbot.score            The total game points collected.
mobbot.science_points   The total science points currently collected.
mobbot.position         The current location of MOB-BOT on the game board.
mobbot.movement_speed   The current movement speed for MOB-BOT.
mobbot.drop_rate        The current drop rate for MOB-BOT.
mobbot.abilities        The current list of abilities MOB-BOT can use.
======================= ==================================================

Methods
-------
Along with these attributes, your MOB-BOT will come pre-loaded with state-of-the-art methods to help you! This includes:

=========================================== ========================================================================================================
Methods                                     Descriptions
=========================================== ========================================================================================================
mobbot.is_researched(tech_name)             Takes in a specified tech enum and returns a boolean of whether or not the tech is currently researched.
mobbot.get_researched_techs()               Returns a list of strings representing all of the currently researched techs.
mobbot.get_all_tech_names()                 Returns a list of strings representing all of the techs in the tech tree.
mobbot.get_tech_info(tech_name)             Takes in a specified tech enum and returns information on the tech.
mobbot.can_place_dynamite()                 Returns a boolean representing if the MOB-BOT can currently use the Dynamite Ability.
mobbot.can_place_landmine()                 Returns a boolean representing if the MOB-BOT can currently use the Landmine Ability.
mobbot.can_place_emp()                      Returns a boolean representing if the MOB-BOT can currently use the EMP Ability.
mobbot.can_defuse_trap()                    Returns a boolean representing if the MOB-BOT can currently use the Defuse Trap Ability.
mobbot.get_company()                        Returns the company enum of your MOB-BOT.
mobbot.get_opposing_team()                  Returns the company enum of the opponents MOB-BOT.
=========================================== ========================================================================================================
