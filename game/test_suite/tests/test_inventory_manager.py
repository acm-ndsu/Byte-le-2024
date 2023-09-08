import unittest

from game.common.enums import Company
from game.common.items.item import Item
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    """
    This class is to test the InventoryManager class and its methods.
    """

    def setUp(self):
        self.manager: InventoryManager = InventoryManager()
        self.item_1: Item = Item(science_point_value=5, value=5)
        self.item_2: Item = Item(science_point_value=5, value=5)
        self.item_3: Item = Item(science_point_value=5, value=5)

    # Tests that cashing in science points works
    def test_cash_sci_points(self):
        self.manager.give(self.item_1, Company.CHURCH)
        self.assertEqual(self.manager.cash_in_science(Company.CHURCH), 5)

    # Tests that cashing in points works
    def test_cash_points(self):
        self.manager.give(self.item_1, Company.CHURCH)
        self.assertEqual(self.manager.cash_in_points(Company.CHURCH), 5)

    def test_inventory_manager_json(self):
        data: dict = self.manager.to_json()
        manager: InventoryManager = InventoryManager().from_json(data)
        self.assertEqual(self.manager.object_type, manager.object_type)
        self.assertEqual(self.manager.get_inventory(Company.CHURCH), manager.get_inventory(Company.CHURCH))
        self.assertEqual(self.manager.get_inventory(Company.TURING), manager.get_inventory(Company.TURING))
