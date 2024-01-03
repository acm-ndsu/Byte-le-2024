import unittest
from game.quarry_rush.ability.dynamite_active_ability import DynamiteActiveAbility


class TestDynamiteActiveAbility(unittest.TestCase):
    """
    This is class that tests the Dynamite Active Ability
    """

    # set up
    def setUp(self) -> None:
        self.dynamite_active_ability = DynamiteActiveAbility()
        self.cooldown: int = 1

    # test: cooldown
    def test_cooldown(self):
        self.cooldown = 1
        self.dynamite_active_ability.cooldown = 1
        self.assertEqual(self.dynamite_active_ability.cooldown, self.cooldown)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown cannot be negative')

    # test: fuse
    def test_fuse(self):
        self.fuse = 1
        self.dynamite_active_ability.fuse = 1
        self.assertEqual(self.dynamite_active_ability.fuse, self.fuse)

    # fail test: fuse CANT be null
    def test_fuse_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.fuse = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.fuse must be an int')

    # fail test: fuse cannot be anything else
    def test_fuse_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.fuse = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.fuse must be an int')

    # fail test: fuse cannot be negative
    def test_fuse_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.fuse = -1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.fuse cannot be negative')

    # test: for placing dynamite
    def test_placing_dynamite(self):
        self.dynamite_active_ability.placing_dynamite = False
        self.assertEqual(self.dynamite_active_ability.placing_dynamite, False)

    # test: json
    def test_dynamite_active_ability_json(self):
        data: dict = self.dynamite_active_ability.to_json()
        dynamite_active_ability: DynamiteActiveAbility = DynamiteActiveAbility().from_json(data)
        self.assertEqual(self.dynamite_active_ability.cooldown, dynamite_active_ability.cooldown)
        self.assertEqual(self.dynamite_active_ability.fuse, dynamite_active_ability.fuse)
        self.assertEqual(self.dynamite_active_ability.object_type, dynamite_active_ability.object_type)
