import unittest
from game.quarry_rush.ability.landmine_active_ability import LandmineActiveAbility
from game.utils.vector import Vector


class TestLandmineActiveAbility(unittest.TestCase):
    """
    This is class that tests the Landmine Active Ability
    """

    # set up
    def setUp(self) -> None:
        self.landmine_active_ability: LandmineActiveAbility = LandmineActiveAbility()

    # test: cooldown
    def test_cooldown(self):
        self.landmine_active_ability.cooldown = 1
        self.assertEqual(self.landmine_active_ability.cooldown, 1)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.cooldown cannot be negative')

    # test: fuse
    def test_fuse(self):
        self.fuse = 1
        self.landmine_active_ability.fuse = 1
        self.assertEqual(self.landmine_active_ability.fuse, self.fuse)

    # fail test: fuse CANT be null
    def test_fuse_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.fuse = None
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.fuse must be an int')

    # fail test: fuse cannot be anything else
    def test_fuse_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.fuse = ""
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.fuse must be an int')

    # fail test: fuse cannot be negative
    def test_fuse_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.landmine_active_ability.fuse = -1
        self.assertEqual(str(e.exception), 'LandmineActiveAbility.fuse cannot be negative')

    # test: json
    def test_landmine_active_ability_json(self):
        data: dict = self.landmine_active_ability.to_json()
        landmine_active_ability: LandmineActiveAbility = LandmineActiveAbility().from_json(data)
        self.assertEqual(self.landmine_active_ability.cooldown, landmine_active_ability.cooldown)
        self.assertEqual(self.landmine_active_ability.fuse, landmine_active_ability.fuse)
        self.assertEqual(self.landmine_active_ability.object_type, landmine_active_ability.object_type)
