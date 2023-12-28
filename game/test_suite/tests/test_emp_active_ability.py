import unittest
from game.quarry_rush.ability.emp_active_ability import EMPActiveAbility


class TestEMPActiveAbility(unittest.TestCase):
    """
    This is class that tests the Trap Defusal Active Ability
    """

    # set up
    def setUp(self) -> None:
        self.emp_active_ability: EMPActiveAbility = EMPActiveAbility()

    # test: cooldown
    def test_cooldown(self):
        self.emp_active_ability.cooldown = 1
        self.assertEqual(self.emp_active_ability.cooldown, 1)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'EMPActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'EMPActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'EMPActiveAbility.cooldown cannot be negative')

    # test: fuse
    def test_fuse(self):
        self.fuse = 1
        self.emp_active_ability.fuse = 1
        self.assertEqual(self.emp_active_ability.fuse, self.fuse)

    # fail test: fuse CANT be null
    def test_fuse_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.fuse = None
        self.assertEqual(str(e.exception), 'EMPActiveAbility.fuse must be an int')

    # fail test: fuse cannot be anything else
    def test_fuse_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.fuse = ""
        self.assertEqual(str(e.exception), 'EMPActiveAbility.fuse must be an int')

    # fail test: fuse cannot be negative
    def test_fuse_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.emp_active_ability.fuse = -1
        self.assertEqual(str(e.exception), 'EMPActiveAbility.fuse cannot be negative')

    # test: json
    def test_emp_active_ability_json(self):
        data: dict = self.emp_active_ability.to_json()
        emp_active_ability: EMPActiveAbility = EMPActiveAbility().from_json(data)
        self.assertEqual(self.emp_active_ability.cooldown, emp_active_ability.cooldown)
        self.assertEqual(self.emp_active_ability.fuse, emp_active_ability.fuse)
        self.assertEqual(self.emp_active_ability.object_type, emp_active_ability.object_type)
