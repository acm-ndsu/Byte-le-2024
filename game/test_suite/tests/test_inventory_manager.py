import unittest

from game.common.enums import Company
from game.common.items.item import Item
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ores import Lambdium, Turite
from game.quarry_rush.entity.ancient_tech import AncientTech


class TestInventoryManager(unittest.TestCase):
    """
    This class is to test the InventoryManager class and its methods.
    """

    def setUp(self):
        self.manager: InventoryManager = InventoryManager()
        self.item_1: Item = Lambdium()
        self.item_2: Item = Turite()
        self.item_3: Item = AncientTech()

    # Tests that cashing in science points works
    def test_cash_sci_points(self):
        self.manager.give(self.item_3, Company.CHURCH)
        self.assertEqual(self.manager.cash_in_science(Company.CHURCH), 10)

    # Tests that cashing in points works
    def test_cash_points(self):
        self.manager.give(self.item_1, Company.CHURCH)
        self.manager.give(self.item_2, Company.CHURCH)
        self.assertEqual(self.manager.cash_in_points(Company.CHURCH), 13)

    def test_inventory_manager_json(self):
        data: dict = self.manager.to_json()
        manager: InventoryManager = InventoryManager().from_json(data)
        self.assertEqual(self.manager.object_type, manager.object_type)
        self.assertEqual(self.manager.get_inventory(Company.CHURCH), manager.get_inventory(Company.CHURCH))
        self.assertEqual(self.manager.get_inventory(Company.TURING), manager.get_inventory(Company.TURING))
