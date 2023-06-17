import unittest

from game.controllers.movement_controller import MovementController
from game.common.map.game_board import GameBoard
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.player import Player
from game.common.avatar import Avatar
from game.common.action import ActionType
from game.common.game_object import GameObject


class TestMovementControllerIfStations(unittest.TestCase):
    def setUp(self) -> None:
        self.movement_controller = MovementController()
        # (1, 0), (2, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 1), (3, 2)
        self.locations: dict = {(Vector(1, 0), Vector(2, 0), Vector(0, 1), Vector(0, 2), Vector(1, 3), Vector(2, 3),
                                 Vector(3, 1), Vector(3, 2)): [Station(None), Station(None), Station(None),
                                                               Station(None), Station(None), Station(None),
                                                               Station(None), Station(None)]}

        self.occ_station = OccupiableStation()
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)
        self.wall = Wall()
        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there \/
        self.avatar = Avatar(position=Vector(2, 2))
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # if there is a station
    def test_move_up_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    def test_move_down_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))

    def test_move_left_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    def test_move_right_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))
