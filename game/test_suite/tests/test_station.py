import unittest

from game.common.stations.station import Station
from game.common.stations.station_example import StationExample
from game.common.items.item import Item
from game.controllers.inventory_controller import InventoryController
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector
from game.common.enums import ActionType
from game.common.enums import ObjectType

# class that tests stations and its methods
class TestStation(unittest.TestCase):
    def setUp(self) -> None:
        self.station = Station()
        self.item = Item(10, 10, 10, 2, 64)
        self.station_example = StationExample(self.item)
        self.avatar = Avatar(Vector(2, 2), 10)
        self.inventory: list[Item] = [Item(0), Item(1), Item(2), Item(3), Item(4), Item(5), Item(6), Item(7), Item(8), Item(9)]
        self.player = Player(avatar=self.avatar)
        self.avatar.inventory = self.inventory
        self.game_board = GameBoard(None, Vector(4, 4), None, False)
        self.inventory_controller = InventoryController()

    # test adding item to station
    def test_item_occ(self):
        self.station.held_item = self.item
        self.assertEqual(self.station.held_item.object_type, ObjectType.ITEM)

    # test adding something not an item
    def test_item_occ_fail(self):
        with self.assertRaises(ValueError) as e:
            self.station.held_item = 'wow'
        self.assertEqual(str(e.exception), 'Station.held_item must be an Item or None, not wow.')

    # test base take action method works
    def test_take_action(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_0, self.player, self.game_board)
        self.station_example.take_action(self.avatar)
        self.assertEqual(self.avatar.held_item.object_type, self.item.object_type)

    # test json method
    def test_json(self):
        self.station.held_item = self.item
        data: dict = self.station.to_json()
        station: Station = Station().from_json(data)
        self.assertEqual(self.station.object_type, station.object_type)
        self.assertEqual(self.station.held_item.object_type, station.held_item.object_type)