import unittest

from game.quarry_rush.station.company_station import CompanyStation
from game.common.avatar import Avatar
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.common.enums import Company
from game.utils.vector import Vector
from game.quarry_rush.entity.ore import Ore


class TestCompanyStation(unittest.TestCase):
    """
    This class is to test the CompanyStation class and its methods.
    """

    def setUp(self) -> None:
        self.turing_station: CompanyStation = CompanyStation(Company.TURING)
        self.church_station: CompanyStation = CompanyStation(Company.CHURCH)
        self.avatar: Avatar = Avatar(Company.CHURCH, Vector(0, 0))
        self.inventory_manager: InventoryManager = InventoryManager()

    # test company attribute of company station
    def test_fail_company_station(self) -> None:
        with self.assertRaises(ValueError) as e:
            self.turing_station.company = 12
        self.assertEqual(str(e.exception), 'CompanyStation.company must be a Company.')

    def test_clear_inventory_company_station(self) -> None:
        self.inventory_manager.give(Ore(), Company.CHURCH)
        self.church_station.take_action(self.avatar, self.inventory_manager)
        self.assertEqual(InventoryManager().is_empty(self.avatar.company), self.inventory_manager.is_empty(self.avatar.company))

    def test_fail_clear_inventory_company_station(self) -> None:
        self.inventory_manager.give(Ore(), Company.CHURCH)
        self.turing_station.take_action(self.avatar, self.inventory_manager)
        inventory2: InventoryManager = InventoryManager()
        inventory2.give(Ore(), Company.CHURCH)
        self.assertEqual(inventory2.is_empty(self.avatar.company), self.inventory_manager.is_empty(self.avatar.company))
