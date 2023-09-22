import unittest

from game.common.enums import *
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.items.item import Item
from game.controllers.inventory_controller import InventoryController
from game.common.map.game_board import GameBoard


class TestInventoryController(unittest.TestCase):
    """
    `Test Inventory Controller Notes:`

        This class tests the different methods in the Avatar class' inventory.
    """

    def setUp(self) -> None:
        self.inventory_controller: InventoryController = InventoryController()
        self.item: Item = Item()
        self.avatar: Avatar = Avatar()

        self.inventory: [Item] = [Item(1), Item(2), Item(3), Item(4), Item(5), Item(6), Item(7), Item(8),
                                  Item(9), Item(10)]

        self.avatar.inventory = self.inventory
        self.player: Player = Player(avatar=self.avatar)
        self.game_board: GameBoard = GameBoard()
