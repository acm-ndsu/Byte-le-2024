import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.defuse_controller import DefuseController
from game.quarry_rush.entity.placeable.traps import Landmine, EMP
from game.utils.vector import Vector


class TestDefuseController(unittest.TestCase):
    def setUp(self):
        self.avatar: Avatar = Avatar()
        self.avatar.science_points = 5000  # to unlock trap defusal
        self.avatar.buy_new_tech('Improved Mining')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')
        self.avatar.buy_new_tech('Trap Defusal')

        self.defuse_controller: DefuseController = DefuseController()
        self.locations: dict[tuple[Vector], list[GameObject]] = {
            (Vector(1, 0),): [Landmine()],  # above avatar
            (Vector(0, 1),): [EMP()],  # left of avatar
            (Vector(1, 1),): [self.avatar],  # center
            (Vector(2, 1),): [EMP()],  # right of avatar
            (Vector(1, 2),): [Landmine()]  # below avatar
        }

        # make a 3x3 game board
        self.world: GameBoard = GameBoard(0, Vector(3, 3), self.locations, False)
        self.client = Player(None, None, [], self.avatar)
        self.world.generate_map()

    # test defusing a trap above works
    def test_defuse_trap(self):
        self.assertTrue(self.world.game_map[0][1].is_occupied_by_game_object(Landmine))
        self.defuse_controller.handle_actions(ActionType.DEFUSE, self.client, self.world)
        self.assertFalse(self.world.game_map[0][1].is_occupied_by_game_object(Landmine))  # remember (y, x) coordinates

    # test defusing the same spot causes no errors
    def test_defuse_twice(self):
        self.test_defuse_trap()
        self.assertFalse(self.world.game_map[0][1].is_occupied_by_game_object(Landmine))