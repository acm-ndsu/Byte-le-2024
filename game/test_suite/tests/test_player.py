import unittest
from game.common.player import Player
from game.common.enums import *
from game.common.avatar import Avatar


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.object_type: ObjectType = ObjectType.PLAYER
        self.functional: bool = True
        self.player: Player = Player()
        self.actions: list[ActionType] = []
        self.team_name: str | None = ""
        self.avatar: Avatar | None = Avatar()

    # test action
    def test_actions(self):
        # accepts a list of ActionType
        self.actions = [ActionType.MOVE_LEFT]
        self.player.actions = self.actions
        self.assertEqual(self.player.actions, self.actions)

    def test_actions_empty_list(self):
        # accepts a list of ActionType
        self.actions = []
        self.player.actions = self.actions
        self.assertEqual(self.player.actions, self.actions)

    def test_actions_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.player.actions = None
        self.assertEqual(str(e.exception), 'Player.action must be an empty list or a list of action types')

    def test_actions_fail_not_action_type(self):
        with self.assertRaises(ValueError) as e:
            self.player.actions = 10
        self.assertEqual(str(e.exception), 'Player.action must be an empty list or a list of action types')

    # test functional
    def test_functional_true(self):
        # functional can only be a boolean
        self.player.functional = True
        self.functional = True
        self.assertEqual(self.player.functional, self.functional)

    #
    def test_functional_false(self):
        self.player.functional = False
        self.functional = False
        self.assertEqual(self.player.functional, self.functional)

    def test_functional_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.player.functional = "String"
        self.assertEqual(str(e.exception), 'Player.functional must be a boolean')

    # team name
    def test_team_name(self):
        # if it is a string it passes
        self.team_name = ""
        self.player.team_name = ""
        self.assertEqual(self.player.team_name, self.team_name)

    def test_team_name_none(self):
        # if it is none it passes
        self.team_name = None
        self.assertEqual(self.player.team_name, self.team_name)

    def test_team_name_fail_int(self):
        # if it is not a string it fails
        with self.assertRaises(ValueError) as e:
            self.player.team_name = 1
        self.assertEqual(str(e.exception), 'Player.team_name must be a String or None')

    # test avatar
    def test_avatar(self):
        self.avatar = Avatar()
        self.player.avatar = self.avatar
        self.assertEqual(self.player.avatar, self.avatar)

    def test_avatar_none(self):
        self.avatar = None
        self.assertEqual(self.player.avatar, self.avatar)

    def test_avatar_fail_string(self):
        with self.assertRaises(ValueError) as e:
            self.player.avatar = 10
        self.assertEqual(str(e.exception), 'Player.avatar must be Avatar or None')

    # test object type
    def test_object_type(self):
        # object type only accepts object type
        self.object_type = ObjectType.PLAYER
        self.player.object_type = self.object_type
        self.assertEqual(self.player.object_type, self.object_type)

    def test_object_type_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.player.object_type = None
        self.assertEqual(str(e.exception), 'Player.object_type must be ObjectType')

    def test_object_type_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.player.object_type = 10
        self.assertEqual(str(e.exception), 'Player.object_type must be ObjectType')

    # test to json
    def test_player_json(self):
        data: dict = self.player.to_json()
        player: Player = Player().from_json(data)
        self.assertEqual(self.player.object_type, player.object_type)
        self.assertEqual(self.player.functional, player.functional)
        self.assertEqual(self.player.team_name, player.team_name)
        self.assertEqual(self.player.actions, player.actions)
        self.assertEqual(self.player.avatar, player.avatar)
