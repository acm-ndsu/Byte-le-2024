import unittest
from game.quarry_rush.ability.active_ability import ActiveAbility


class TestActiveAbility(unittest.TestCase):

    """
    This is class that tests the Active Ability
    """
    # set up
    def setUp(self) -> None:
        self.active_ability = ActiveAbility()
        self.cooldown: int = 1

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

    # test: fuse
    def test_fuse(self):
        self.fuse = 1
        self.active_ability.fuse = 1
        self.assertEqual(self.active_ability.fuse, self.fuse)

    # fail test: fuse CANT be null
    def test_fuse_fail_null(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.fuse = None
        self.assertEqual(str(e.exception), 'ActiveAbility.fuse must be an int')

    # fail test: fuse cannot be anything else
    def test_fuse_fail_str(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.fuse = ""
        self.assertEqual(str(e.exception), 'ActiveAbility.fuse must be an int')

    # fail test: fuse cannot be negative
    def test_fuse_fail_negative(self):
        with self.assertRaises(ValueError) as e:
            self.active_ability.fuse = -1
        self.assertEqual(str(e.exception), 'ActiveAbility.fuse cannot be negative')

    # test is_useable: 0 = true
    def test_is_useable_true(self):
        self.active_ability.fuse = 0
        self.assertEqual(self.active_ability.is_useable(), True)

    # test is_useable: any other number = false
    def test_is_useable_false(self):
        self.active_ability.fuse = 1
        self.assertEqual(self.active_ability.is_useable(), False)

    # test decrease_fuse
    def test_decrease_fuse(self):
        self.active_ability.decrease_fuse()
        self.assertEqual(self.active_ability.fuse, 0)  # check to make decremented properly

    # test decrease_fuse: CANT be negative
    def test_decrease_fuse_fail_negative(self):
        self.active_ability.fuse = 0
        self.active_ability.decrease_fuse()
        self.assertEqual(self.active_ability.fuse, 0)

    # test reset cooldown tick: testing to reset it back to the original cooldown variable
    def test_reset_fuse(self):
        self.active_ability.fuse = 0
        self.active_ability.reset_fuse()
        self.assertEqual(self.active_ability.fuse, 1)

    # test: json
    def test_active_ability_json(self):
        data: dict = self.active_ability.to_json()
        active_ability: ActiveAbility = ActiveAbility().from_json(data)
        self.assertEqual(self.active_ability.cooldown, active_ability.cooldown)
        self.assertEqual(self.active_ability.fuse, active_ability.fuse)
        self.assertEqual(self.active_ability.object_type, active_ability.object_type)
