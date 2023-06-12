import unittest

from game.common.enums import *
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.items.item import Item
from game.controllers.inventory_controller import InventoryController
from game.common.map.game_board import GameBoard


class TestInventoryController(unittest.TestCase):
    """
    This class is to test the InventoryController class and its methods.
    """

    def setUp(self) -> None:
        self.inventory_controller: InventoryController = InventoryController()
        self.item: Item = Item()
        self.avatar: Avatar = Avatar()

        self.inventory: list[Item] = [Item(1), Item(2), Item(3), Item(4), Item(5), Item(6), Item(7), Item(8),
                                  Item(9), Item(10)]

        self.avatar.inventory = self.inventory
        self.player: Player = Player(avatar=self.avatar)
        self.game_board: GameBoard = GameBoard()

    # Testing accessing the right Item with the controller
    def test_select_slot_0(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_0, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[0])
        self.check_inventory_item()

    def test_select_slot_1(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_1, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[1])
        self.check_inventory_item()

    def test_select_slot_2(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_2, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[2])
        self.check_inventory_item()

    def test_select_slot_3(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_3, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[3])
        self.check_inventory_item()

    def test_select_slot_4(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_4, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[4])
        self.check_inventory_item()

    def test_select_slot_5(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_5, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[5])
        self.check_inventory_item()

    def test_select_slot_6(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_6, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[6])
        self.check_inventory_item()

    def test_select_slot_7(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_7, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[7])
        self.check_inventory_item()

    def test_select_slot_8(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_8, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[8])
        self.check_inventory_item()

    def test_select_slot_9(self):
        self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_9, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.inventory[9])
        self.check_inventory_item()

    # Testing using the inventory controller with the wrong ActionType
    def test_with_wrong_action_type(self):
        self.inventory_controller.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.assertEqual(self.avatar.held_item, self.avatar.inventory[0])
        self.check_inventory_item()

    # Tests accessing a slot of the inventory given an enum that's out of bounds
    def test_with_out_of_bounds(self):
        with self.assertRaises(IndexError) as e:
            self.inventory: list[Item] = [Item(1), Item(2), Item(3), Item(4), Item(5)]
            self.avatar.max_inventory_size = 5
            self.avatar.inventory = self.inventory
            self.player: Player = Player(avatar=self.avatar)
            self.inventory_controller.handle_actions(ActionType.SELECT_SLOT_9, self.player, self.game_board)
        self.assertEqual(str(e.exception), 'The given action type, SELECT_SLOT_9, is not within bounds of the given '
                                           'inventory of size 5. Select an ActionType enum '
                                           'that will be within the inventory\'s bounds.')

    def check_inventory_item(self):
        # Test to make sure that the inventory hasn't shifted items
        self.assertEqual(self.avatar.inventory[0].value, 1)
        self.assertEqual(self.avatar.inventory[1].value, 2)
        self.assertEqual(self.avatar.inventory[2].value, 3)
        self.assertEqual(self.avatar.inventory[3].value, 4)
        self.assertEqual(self.avatar.inventory[4].value, 5)
        self.assertEqual(self.avatar.inventory[5].value, 6)
        self.assertEqual(self.avatar.inventory[6].value, 7)
        self.assertEqual(self.avatar.inventory[7].value, 8)
        self.assertEqual(self.avatar.inventory[8].value, 9)
        self.assertEqual(self.avatar.inventory[9].value, 10)
