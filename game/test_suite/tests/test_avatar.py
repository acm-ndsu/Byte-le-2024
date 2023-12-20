import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector


class TestAvatar(unittest.TestCase):
    """
    `Test Avatar Notes:`

        This class tests the different methods in the Avatar class.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar()
        self.item: Item = Item(10, 100, 1, 1)

    # test set score
    def test_avatar_set_score(self):
        self.avatar.score = 10
        self.assertEqual(self.avatar.score, 10)

    def test_avatar_set_score_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.score = 'wow'
        self.assertEqual(str(e.exception), 'Avatar.score must be an int.')

    # test set position
    def test_avatar_set_position(self):
        self.avatar.position = Vector(10, 10)
        self.assertEqual(str(self.avatar.position), str(Vector(10, 10)))

    def test_avatar_set_position_None(self):
        self.avatar.position = None
        self.assertEqual(self.avatar.position, None)

    def test_avatar_set_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.position = 10
        self.assertEqual(str(e.exception), 'Avatar.position must be a Vector or None.')

    # test json method
    def test_avatar_json_with_none_item(self):
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    def test_avatar_json_with_item(self):
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.position.object_type, avatar.position.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    # Quarry Rush tests below ------------------------------------------------------------------------------------------

    # Test setting score to be negative
    def test_set_score_negative(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.score = -1
        self.assertEqual(str(e.exception), 'Avatar.score must be a positive int.')

    # Test setting movement speed
    def test_avatar_set_movement_speed(self):
        self.avatar.movement_speed = 5
        self.assertEqual(self.avatar.movement_speed, 5)

    def test_avatar_set_movement_speed_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.movement_speed = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.movement_speed must be an int.')

    def test_movement_speed_negative(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.movement_speed = -1
        self.assertEqual(str(e.exception), 'Avatar.movement_speed must be a positive int.')

    # Test setting science_points
    def test_avatar_set_science_points(self):
        self.avatar.science_points = 5
        self.assertEqual(self.avatar.science_points, 5)

    def test_avatar_set_science_points_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.science_points = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.science_points must be an int.')

    def test_set_science_points_negative(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.science_points = -1
        self.assertEqual(str(e.exception), 'Avatar.science_points must be a positive int.')

    # Test setting drop rate
    def test_avatar_set_drop_rate(self):
        self.avatar.drop_rate = 5.3
        self.assertEqual(self.avatar.drop_rate, 5.3)

    def test_avatar_set_drop_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.drop_rate = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.drop_rate must be a float.')

    def test_drop_rate_negative(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.drop_rate = -1.0
        self.assertEqual(str(e.exception), 'Avatar.drop_rate must be a positive float.')

    # Testing which techs are unlocked
    def test_unlocked_tech(self):
        self.assertTrue(self.avatar.is_researched('Mining Robotics'))
        self.assertFalse(self.avatar.is_researched('Better Drivetrains'))
        self.assertFalse(self.avatar.is_researched('Dynamite'))

    # Buying Overdrive Movement will return False if the tree hasn't developed to it yet
    def test_unlock_overdrive_movement_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('Overdrive Movement'))

    # Tests that unlocking Overdrive Movement works
    def test_unlock_overdrive_movement(self):
        self.avatar.buy_new_tech('Better Drivetrains')
        self.avatar.buy_new_tech('Unnamed Drivetrain Tech')
        self.avatar.buy_new_tech('Overdrive Movement')
        self.assertTrue(self.avatar.is_researched('Better Drivetrains'))
        self.assertTrue(self.avatar.is_researched('Unnamed Drivetrain Tech'))
        self.assertTrue(self.avatar.is_researched('Overdrive Movement'))

    # Buying Overdrive Mining will return False if the tree hasn't developed to it yet
    def test_unlock_overdrive_mining_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('Overdrive Mining'))

    # Tests that unlocking Overdrive Mining works
    def test_unlock_overdrive_mining(self):
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Unnamed Mining Tech')
        self.avatar.buy_new_tech('Overdrive Mining')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Unnamed Mining Tech'))
        self.assertTrue(self.avatar.is_researched('Overdrive Mining'))

    # Buying Dynamite will return False if the tree hasn't developed to it yet
    def test_unlock_dynamite_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('Dynamite'))

    # Tests that unlocking Dynamite works
    def test_unlock_dynamite(self):
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Dynamite')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))

    # Buying Landmines will return False if the tree hasn't developed to it yet
    def test_unlock_landmines_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('Landmines'))

    # Tests that unlocking Landmines works
    def test_unlock_landmines(self):
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))

    # Buying EMPs will return False if the tree hasn't developed to it yet
    def test_unlock_emps_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('EMPs'))

    # Tests that unlocking EMPs works and that unlocking Trap Detection returns False
    def test_unlock_emps(self):
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')
        self.avatar.buy_new_tech('EMPs')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))
        self.assertTrue(self.avatar.is_researched('EMPs'))
        self.assertFalse(self.avatar.is_researched('Trap Defusal'))

    # Buying Trap Detection will return False if the tree hasn't developed to it yet
    def test_unlock_trap_defusal_fail(self):
        self.assertFalse(self.avatar.buy_new_tech('Trap Defusal'))

    # Tests that unlocking Trap Defusal works and that unlocking EMPs returns False
    def test_unlock_trap_defusal(self):
        self.avatar.buy_new_tech('High Yield Drilling')
        self.avatar.buy_new_tech('Dynamite')
        self.avatar.buy_new_tech('Landmines')
        self.avatar.buy_new_tech('Trap Defusal')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))
        self.assertTrue(self.avatar.is_researched('Trap Defusal'))
        self.assertFalse(self.avatar.is_researched('EMPs'))

    # Tests getting the researched techs
    def test_get_researched_techs(self):
        self.assertEqual(self.avatar.get_researched_techs(), ['Mining Robotics'])
        self.avatar.buy_new_tech('Better Drivetrains')
        self.assertEqual(self.avatar.get_researched_techs(), ['Mining Robotics', 'Better Drivetrains'])

    # Test the json with the new implementations
    def test_avatar_json(self):
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.score, avatar.score)
        self.assertEqual(self.avatar.science_points, avatar.science_points)
        self.assertEqual(str(self.avatar.position), str(avatar.position))
        self.assertEqual(self.avatar.movement_speed, avatar.movement_speed)
        self.assertEqual(self.avatar.drop_rate, avatar.drop_rate)

        # other_tree: dict = self.avatar.get_tech_tree().to_json()
        # for tech in self.avatar.get_tech_tree().tech_names():
        #     self.assertEqual(other_tree[tech], self.avatar.get_tech_tree().is_researched(tech))
        # self.assertEqual(self.avatar.get_tech_tree().avatar_functions, other_tree['avatar_functions'])
