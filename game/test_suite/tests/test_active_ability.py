import unittest
from game.quarry_rush.active_ability import ActiveAbility
from game.common.avatar import Avatar


class TestActiveAbility(unittest.TestCase):

    """
    This is class that tests the Active Ability
    """
    # set up
    def setUp(self) -> None:
        self.active_ability = ActiveAbility()
        self.name: str = ""
        self.cooldown: int = 1

    # test: name
    def test_name(self):
        self.name = ""
        self.active_ability.name = ""
        self.assertEqual(self.active_ability.name, self.name)

    # fail test: name CANT be null
    def test_name_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.name = None
        self.assertEqual(str(e.exception), 'ActiveAbility.name must be a String')

    # fail test: name cant be anything else
    def test_name_fail_int(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.name = 1
        self.assertEqual(str(e.exception), 'ActiveAbility.name must be a String')

    # test: avatar
    def test_avatar(self):
        self.avatar = Avatar()
        self.active_ability.avatar = self.avatar
        self.assertEqual(self.active_ability.avatar, self.avatar)

    # test: avatar none
    def test_avatar_none(self):
        self.avatar = None
        self.active_ability.avatar = self.avatar
        self.assertEqual(self.active_ability.avatar, self.avatar)

    # fail test: avatar cannot be anything else
    def test_avatar_fail(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.avatar = ""
        self.assertEqual(str(e.exception), 'ActiveAbility.avatar must be Avatar or None')

    # test: cooldown
    def test_cooldown(self):
        self.cooldown = 1
        self.active_ability.cooldown = 1
        self.assertEqual(self.active_ability.cooldown, self.cooldown)

    # fail test: cooldown CANT be null
    def test_cooldown_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown = None
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown must be an int')

    # fail test: cooldown cant be anything else
    def test_cooldown_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown = ""
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown must be an int')

    # fail test: cooldown cannot be negative
    def test_cooldown_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown = -1
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown cannot be negative')

    # test: cooldown_tick
    def test_cooldown_tick(self):
        self.cooldown_tick = 1
        self.active_ability.cooldown_tick = 1
        self.assertEqual(self.active_ability.cooldown_tick, self.cooldown_tick)

    # fail test: cooldown_tick CANT be null
    def test_cooldown_tick_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown_tick = None
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be anything else
    def test_cooldown_tick_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown_tick = ""
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown_tick must be an int')

    # fail test: cooldown_tick cannot be negative
    def test_cooldown_tick_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.cooldown_tick = -1
        self.assertEqual(str(e.exception), 'ActiveAbility.cooldown_tick cannot be negative')

    # test is_useable: 0 = true
    def test_is_useale_true(self):
        self.active_ability.cooldown_tick = 0
        self.assertEqual(self.active_ability.is_useable(), True)

    # test is_useable: any other number = false
    def test_is_useale_false(self):
        self.active_ability.cooldown_tick = 1
        self.assertEqual(self.active_ability.is_useable(), False)

    # test decrease_cooldown_tick
    def test_decrease_cooldown_tick(self):
        self.active_ability.decrease_cooldown_tick()
        self.assertEqual(self.active_ability.cooldown_tick, 0)  # check to make decremented properly

    # test decrease_cooldown_tick: CANT be negative
    def test_decrease_cooldown_tick_fail_negative(self):
        self.active_ability.cooldown_tick = 0
        self.active_ability.decrease_cooldown_tick()
        self.assertEqual(self.active_ability.cooldown_tick, 0)

    # test reset cooldown tick: testing to reset it back to the original cooldown variable
    def test_reset_cooldown_tick(self):
        self.active_ability.cooldown_tick = 0
        self.active_ability.reset_cooldown_tick()
        self.assertEqual(self.active_ability.cooldown_tick, 1)

    # test: json
    def test_active_ability_json(self):
        data: dict = self.active_ability.to_json()
        active_ability: ActiveAbility = ActiveAbility().from_json(data)
        self.assertEqual(self.active_ability.name, active_ability.name)
        self.assertEqual(self.active_ability.cooldown, active_ability.cooldown)
        self.assertEqual(self.active_ability.cooldown_tick, active_ability.cooldown_tick)
        self.assertEqual(self.active_ability.object_type, active_ability.object_type)
