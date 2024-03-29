import unittest

from game.quarry_rush.entity.placeable.traps import *
from game.common.enums import Company
from game.utils.vector import Vector
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class TestTrap(unittest.TestCase):
    """
    This class is to test the generic trap class and its methods for the Byte-le 2024 game
    """

    opponent_position = Vector(2, 2)

    def setUp(self) -> None:
        self.inventory_manager = InventoryManager()
        self.trap = Trap(0.1, Company.CHURCH, Company.TURING,
                         lambda: self.opponent_position, Vector(0, 0))
        self.range = 1
        self.position = Vector(0, 0)

    # test set steal_rate
    def test_set_steal_rate(self):
        self.trap.steal_rate = 0.1
        self.assertEqual(self.trap.steal_rate, 0.1)

    def test_set_steal_rate_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.steal_rate = None
        self.assertEqual(str(e.exception), 'Trap.steal_rate must be a float.')

    def test_set_steal_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.steal_rate = 1
        self.assertEqual(str(e.exception), 'Trap.steal_rate must be a float.')

    # test set owner company
    def test_set_owner_company(self):
        self.trap.owner_company = Company.TURING
        self.assertEqual(self.trap.owner_company, Company.TURING)

    def test_set_owner_company_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.owner_company = None
        self.assertEqual(str(e.exception), 'Trap.owner_company must be of enum type Company.')

    def test_set_owner_company_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.owner_company = 123
        self.assertEqual(str(e.exception), 'Trap.owner_company must be of enum type Company.')

    # test set target company
    def test_set_target_company(self):
        self.trap.target_company = Company.CHURCH
        self.assertEqual(self.trap.target_company, Company.CHURCH)

    def test_set_target_company_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.target_company = None
        self.assertEqual(str(e.exception), 'Trap.target_company must be of enum type Company.')

    def test_set_target_company_int_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.target_company = 123
        self.assertEqual(str(e.exception), 'Trap.target_company must be of enum type Company.')

    # test set opponent_position
    def test_set_opponent_position(self):
        self.opponent_position = Vector(1, 1)
        self.trap.opponent_position = lambda: self.opponent_position
        self.assertEqual(self.trap.opponent_position(), self.opponent_position)
        self.opponent_position = Vector(0, 0)
        self.assertEqual(self.trap.opponent_position(), self.opponent_position)

    def test_set_opponent_position_fail_none(self):
        with self.assertRaises(ValueError) as e:
            self.trap.opponent_position = None
        self.assertEqual(str(e.exception), 'Trap.opponent_position must be of type Callable[[], Vector].')

    def test_set_opponent_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.trap.opponent_position = lambda: 12
        self.assertEqual(str(e.exception), 'Trap.opponent_position must be of type Callable[[], Vector].')

    # test in_range method
    def test_in_range_false(self):
        self.opponent_position = Vector(2, 2)
        self.assertEqual(self.trap.in_range(), False)
        self.opponent_position = Vector(2, 0)
        self.assertEqual(self.trap.in_range(), False)
        self.opponent_position = Vector(1, 1)
        self.assertEqual(self.trap.in_range(), False)


    def test_in_range_true(self):
        self.opponent_position = Vector(0, 0)
        self.assertEqual(self.trap.in_range(), True)
        self.opponent_position = Vector(1, 0)
        self.assertEqual(self.trap.in_range(), True)

    # test detonate method (should have same bool results as in_range method)
    def test_detonate_false(self):
        self.opponent_position = Vector(2, 2)
        self.assertEqual(self.trap.detonate(self.inventory_manager), False)
        self.opponent_position = Vector(2, 0)
        self.assertEqual(self.trap.detonate(self.inventory_manager), False)
        self.opponent_position = Vector(1, 1)
        self.assertEqual(self.trap.detonate(self.inventory_manager), False)

    def test_detonate_true(self):
        self.opponent_position = Vector(0, 0)
        self.assertEqual(self.trap.detonate(self.inventory_manager), True)
        self.opponent_position = Vector(1, 0)
        self.assertEqual(self.trap.detonate(self.inventory_manager), True)

    # test default of Landmine
    def test_landmine(self):
        self.landmine = Landmine(Company.CHURCH, Company.TURING, lambda: self.opponent_position, Vector(1, 1))
        self.assertEqual(self.landmine.steal_rate, 0.5)

    # test default of EMP
    def test_EMP(self):
        self.EMP = EMP(Company.TURING, Company.CHURCH, lambda: self.opponent_position, Vector(2, 2))
        self.assertEqual(self.EMP.steal_rate, 1.0)

    # test json
    def test_trap_json(self):
        data: dict = self.trap.to_json()
        trap: Trap = Trap().from_json(data)
        self.assertEqual(data['steal_rate'], 0.1)
        # inventory_manager not a part of json as there is only one
        with self.assertRaises(KeyError) as e:
            self.assertEqual(data['inventory_manager'], InventoryManager())
        self.assertEqual(str(e.exception), '\'inventory_manager\'')
        self.assertEqual(trap.owner_company.value, Company.CHURCH.value)
        self.assertEqual(trap.target_company.value, Company.TURING.value)
        self.assertEqual(trap.range, self.range)
        self.assertEqual(str(trap.position), str(self.position))

        # To test the object type, need to make a new Trap object
        trap: Trap = Trap().from_json(data)
        self.assertEqual(trap.object_type, self.trap.object_type)
