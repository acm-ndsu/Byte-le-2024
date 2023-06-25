import unittest

from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.player import Player
from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject


class TestMovementControllerIfWall(unittest.TestCase):
    def setUp(self) -> None:
        self.movement_controller = MovementController()
        self.avatar = Avatar(position=Vector(2, 2))
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(2, 2),): [self.avatar]
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)
        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there \/
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # if there is a wall
    def test_move_up(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 3)))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(3, 2)))
