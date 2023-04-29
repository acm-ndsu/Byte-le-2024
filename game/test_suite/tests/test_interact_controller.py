import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.controllers.interact_controller import InteractController
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.game_object import GameObject
from game.common.action import ActionType
from game.common.player import Player
from game.common.enums import ObjectType


class TestInteractController(unittest.TestCase):
    """
    This class is to test the InteractController class and its methods.
    """

    def setUp(self) -> None:
        self.interact_controller: InteractController = InteractController()
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.occupiable_station: OccupiableStation = OccupiableStation(self.item)
        self.avatar: Avatar = Avatar(None, Vector(5, 5))
        self.locations: dict[tuple[Vector]:list[GameObject]] = {
            (Vector(1, 1),): [Station(None)],
            (Vector(5, 4),): [self.occupiable_station],
            (Vector(6, 5),): [Station(self.item)],
            (Vector(4, 5),): [Station(None)],
            (Vector(5, 5),): [self.avatar],
            (Vector(5, 6),): [self.wall]
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.player: Player = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # interact and pick up nothing
    def test_interact_nothing(self):
        self.interact_controller.handle_actions(ActionType.INTERACT_DOWN, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, None)

    # interact and pick up from an occupiable_station 
    def test_interact_item_occupible_station(self):
        self.interact_controller.handle_actions(ActionType.INTERACT_UP, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item.object_type, ObjectType.ITEM)

    # interact and pick up from a station
    def test_interact_item_station(self):
        self.interact_controller.handle_actions(ActionType.INTERACT_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item.object_type, ObjectType.ITEM)

    # interact and get item then dump item
    def test_interact_dump_item(self):
        self.interact_controller.handle_actions(ActionType.INTERACT_RIGHT, self.player, self.game_board)
        self.interact_controller.handle_actions(ActionType.INTERACT_LEFT, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, None)
