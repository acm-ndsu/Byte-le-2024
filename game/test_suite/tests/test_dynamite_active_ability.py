import unittest
from game.quarry_rush.dynamite_active_ability import DynamiteActiveAbility
from game.common.avatar import Avatar


class TestDynamiteActiveAbility(unittest.TestCase):

    """
    This is class that tests the Active Ability
    """
    # set up
    def setUp(self) -> None:
        self.dynamite_active_ability = DynamiteActiveAbility()
        self.name: str = ""
        self.cooldown: int = 1

    # test: name
    def test_name(self):
        self.name = ""
        self.dynamite_active_ability.name = ""
        self.assertEqual(self.dynamite_active_ability.name, self.name)

    # fail test: name CANT be null
    def test_name_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.name = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.name must be a String')

    # fail test: name cant be anything else
    def test_name_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.name = 1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.name must be a String')

    # test: avatar
    def test_avatar(self):
        self.avatar = Avatar()
        self.dynamite_active_ability.avatar = self.avatar
        self.assertEqual(self.dynamite_active_ability.avatar, self.avatar)

    # test: avatar none
    def test_avatar_none(self):
        self.avatar = None
        self.dynamite_active_ability.avatar = self.avatar
        self.assertEqual(self.dynamite_active_ability.avatar, self.avatar)

    # fail test: avatar cannot be anything else
    def test_avatar_fail(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.avatar = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.avatar must be Avatar or None')

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

    # test: cooldown_tick
    def test_cooldown_tick(self):
        self.cooldown_tick = 1
        self.dynamite_active_ability.cooldown_tick = 1
        self.assertEqual(self.dynamite_active_ability.cooldown_tick, self.cooldown_tick)

    # fail test: cooldown_tick CANT be null
    def test_cooldown_tick_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = None
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be anything else
    def test_cooldown_tick_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = ""
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be negative
    def test_cooldown_tick_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.dynamite_active_ability.cooldown_tick = -1
        self.assertEqual(str(e.exception), 'DynamiteActiveAbility.cooldown_tick cannot be negative')

    # test for place dynamite





