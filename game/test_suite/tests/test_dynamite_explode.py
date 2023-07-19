import unittest
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.action import ActionType
from game.common.game_object import GameObject
from game.quarry_rush.dynamite import Dynamite
from game.common.items import item


class TestDynamiteExplode(unittest.TestCase):
    def setUp(self) -> None:
        self.dynamite = Dynamite()
        self.item = item
        self.dynamite.explode()
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(2, 2),): [self.item]
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)
        self.game_board.generate_map()

    # explode above tile
    def explode_up(self):
        self.dynamite.explode().handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
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
