==========
The Server
==========

Here are some notes to consider about the server to aid you in the competiton.


Registering
===========

To register your team, type

.. code-block::

    python launcher.pyz client -register

into the terminal. Follow the prompts to enter your team name, select your university, and select if you are an alumni.

After registering, you will receive a new file called ``vID`` in your Byte-le 2024 folder. **DO NOT SHARE THIS.** This
is unique to your team and allows you to submit your clients and view specific team information.

Client Commands
===============

**NOTE**: As commands are listed, some will have two versions to perform the same task. The first command will be typed
in its entirety, and the second command will be a shortened version for ease of use.

**Only ONE line needs to be typed into the terminal, NOT both.**


Submitting Code
---------------

To submit your client code, type the following into the terminal:

.. code-block::

    python launcher.pyz client -submit
    python launcher.pyz c -submit


After successfully registering your team, you are able to submit your client code. At least one client must be
submitted by 10 PM to be eligible to win. The server automatically looks for files in the root directory that contain
the word 'client,' so you don't need to stress about submitting the correct file.

Once uploaded to the server, your code will run against other submitted code to determine placing. You can submit as
many times as you'd like during the duration of the competition, but do not excessively upload, please.


Leaderboard
-----------

To view the leaderboard, type one of the following in the terminal:

.. code-block::

    python launcher.pyz client leaderboard
    python launcher.pyz c l

These will return the leaderboard for all eligible contestants. By default, alumni are not included. To include
alumni, type one of the following:

.. code-block::

    python launcher.pyz client leaderboard -include_alumni
    python launcher.pyz c l -include_alumni

If you want to see previous leaderboards from the competition, you may type one of the following by providing a
leaderboard's id:

.. code-block::

    python launcher.pyz client leaderboard -leaderboard_id <leaderboard_id>
    python launcher.pyz c l -leaderboard_id <leaderboard_id>


Stats
-----

To view your stats for the latest submission, type

.. code-block::

    python launcher.pyz client stats
    python launcher.pyz c s

to view them. Your stats will continue to change until all games are completed.

If you desire to see all of your submissions, type

.. code-block::

    python launcher.pyz client -get_submissions
    python launcher.pyz c -get_submissions

to receive all your submission ids. These ids can be used in some of the commands listed below.

To view code from a previous submission, have a submission id ready and type

.. code-block::

    python launcher.pyz client -get_code_for_submission <submission_id>
    python launcher.pyz c -get_code_for_submission <submission_id>

to receive the code file from the given submission.


Extra Help
==========

For extra help on these commands, you can type ``-h`` after any of these commands to have the help message appear.
For example:

.. code-block::

    python launcher.pyz client -h
    python launcher.pyz c -h

or

.. code-block::

    python launcher.pyz client leaderboard -h
    python launcher.pyz c l -h

will show you the help descriptions of all client and leaderboard commands respectively.
