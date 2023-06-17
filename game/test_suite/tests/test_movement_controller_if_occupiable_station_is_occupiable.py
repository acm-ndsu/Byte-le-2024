import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.common.player import Player
from game.common.stations.occupiable_station import OccupiableStation
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from game.common.stations.station import Station


class TestMovementControllerIfOccupiableStationIsOccupiable(unittest.TestCase):
    """
    `Test Movement Controller if Occupiable Stations are Occupiable Notes:`

        This class tests the different methods in the Movement Controller class and the Avatar moving onto Occupiable
        Stations so that the Avatar can occupy it.
    """

    def setUp(self) -> None:
        self.movement_controller = MovementController()

        # (1, 0), (2, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 1), (3, 2)
        self.locations: dict = {
            (Vector(1, 0), Vector(2, 0), Vector(0, 1), Vector(0, 2)): [OccupiableStation(None, None),
                                                                       OccupiableStation(None, None),
                                                                       OccupiableStation(None, None),
                                                                       OccupiableStation(None, None)]}
        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)
        self.occ_station = OccupiableStation()
        self.occ_station = OccupiableStation()
        # self.wall = Wall()
        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there \/
        self.avatar = Avatar(position=Vector(1, 1))
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()


def test_move_up(self):
    self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
    self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 0)))


def test_move_down(self):
    self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
    self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))


def test_move_left(self):
    self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
    self.assertEqual((str(self.client.avatar.position)), str(Vector(0, 1)))


def test_move_right(self):
    self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
    self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))
