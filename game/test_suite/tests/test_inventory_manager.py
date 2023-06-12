import unittest

from game.quarry_rush.inventory_manager import InventoryManager
from game.utils.vector import Vector


class TestInventoryManager(unittest.TestCase):
    """
    This class is to test the InventoryManager class and its methods.
    """

    def setUp(self):
        self.manager: InventoryManager = InventoryManager()

    # Test that only one instance of the InventoryManager is created. Will find better way to test this after testing
    def test_one_instance(self):
        new_manager: InventoryManager = InventoryManager()
        self.assertTrue(isinstance(self.manager, InventoryManager))
        self.assertTrue(new_manager is None)
