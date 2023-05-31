import unittest

from game.common.avatar import Avatar, LockedTechError
from game.common.items.item import Item
from game.quarry_rush.tech_tree import TechTree
from game.utils.vector import Vector


class TestAvatar(unittest.TestCase):
    """
    This class is to test the Avatar class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, 1)
        self.item: Item = Item(10, 100, 1, 1)

    # test set item
    def test_avatar_set_item(self):
        self.avatar.pick_up(self.item)
        self.assertEqual(self.avatar.held_item, self.item)

    def test_avatar_set_item_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.held_item = 3
        self.assertEqual(str(e.exception), 'Avatar.held_item must be an Item or None.')

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
        # held item will be None
        self.avatar.held_item = self.avatar.inventory[0]
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item, avatar.held_item)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    def test_avatar_json_with_item(self):
        self.avatar.pick_up(Item(1, 1))
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.held_item.object_type, avatar.held_item.object_type)
        self.assertEqual(self.avatar.held_item.value, avatar.held_item.value)
        self.assertEqual(self.avatar.held_item.durability, avatar.held_item.durability)
        self.assertEqual(self.avatar.position.object_type, avatar.position.object_type)
        self.assertEqual(str(self.avatar.position), str(avatar.position))

    # Quarry Rush tests below ------------------------------------------------------------------------------------------

    # Test setting movement speed
    def test_avatar_set_movement_speed(self):
        self.avatar.movement_speed = 5
        self.assertEqual(self.avatar.movement_speed, 5)

    def test_avatar_set_movement_speed_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.movement_speed = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.movement_speed must be an int.')

    # Test setting drop rate
    def test_avatar_set_drop_rate(self):
        self.avatar.drop_rate = 5.3
        self.assertEqual(self.avatar.drop_rate, 5.3)

    def test_avatar_set_drop_rate_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.drop_rate = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.drop_rate must be a float.')

    # test that getting the tech tree works
    def get_tech_tree(self):
        other_tree: TechTree = self.avatar.get_tech_tree()
        self.assertEqual(self.avatar.get_tech_tree(), other_tree)

    # Testing which techs are unlocked
    def test_unlocked_tech(self):
        self.assertTrue(self.avatar.is_researched('Mining Robotics'))
        self.assertFalse(self.avatar.is_researched('Better Drivetrains'))
        self.assertFalse(self.avatar.is_researched('Dynamite'))

    # Unlocking Overdrive Movement will fail if Unnamed Drivetrain Tech isn't researched
    def test_unlock_overdrive_movement_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_movement_overdrive()
        self.assertEqual(str(e.exception), 'Avatar must unlock Unnamed Drivetrain Tech before using Overdrive '
                                           'Movement.')

    # Tests that unlocking Overdrive Movement works
    def test_unlock_overdrive_movement(self):
        self.avatar.get_tech_tree().research('Better Drivetrains')
        self.avatar.get_tech_tree().research('Unnamed Drivetrain Tech')
        self.avatar.get_tech_tree().research('Overdrive Movement')
        self.assertTrue(self.avatar.is_researched('Better Drivetrains'))
        self.assertTrue(self.avatar.is_researched('Unnamed Drivetrain Tech'))
        self.assertTrue(self.avatar.is_researched('Overdrive Movement'))

    # Fails if Unnamed Mining Tech isn't researched
    def test_unlock_overdrive_mining_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_mining_overdrive()
        self.assertEqual(str(e.exception), 'Avatar must unlock Unnamed Mining Tech before using Overdrive '
                                           'Mining.')

    # Tests that unlocking Overdrive Mining works
    def test_unlock_overdrive_mining(self):
        self.avatar.get_tech_tree().research('High Yield Drilling')
        self.avatar.get_tech_tree().research('Unnamed Mining Tech')
        self.avatar.get_tech_tree().research('Overdrive Mining')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Unnamed Mining Tech'))
        self.assertTrue(self.avatar.is_researched('Overdrive Mining'))

    # Fails if High Yield Drilling isn't researched
    def test_unlock_dynamite_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_dynamite()
        self.assertEqual(str(e.exception), 'Avatar must unlock High Yield Drilling before using Dynamite.')

    # Tests that unlocking Dynamite works
    def test_unlock_dynamite(self):
        self.avatar.get_tech_tree().research('High Yield Drilling')
        self.avatar.get_tech_tree().research('Dynamite')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))

    # Fails if Dynamite isn't researched
    def test_unlock_landmines_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_landmines()
        self.assertEqual(str(e.exception), 'Avatar must unlock Dynamite before using Landmines.')

    # Tests that unlocking Landmines works
    def test_unlock_landmines(self):
        self.avatar.get_tech_tree().research('High Yield Drilling')
        self.avatar.get_tech_tree().research('Dynamite')
        self.avatar.get_tech_tree().research('Landmines')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))

    # Fails if Landmines aren't researched
    def test_unlock_emps_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_emps()
        self.assertEqual(str(e.exception), 'Avatar must unlock Landmines before using EMPs.')

    # Tests that unlocking EMPs works
    def test_unlock_emps(self):
        self.avatar.get_tech_tree().research('High Yield Drilling')
        self.avatar.get_tech_tree().research('Dynamite')
        self.avatar.get_tech_tree().research('Landmines')
        self.avatar.get_tech_tree().research('EMPs')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))
        self.assertTrue(self.avatar.is_researched('EMPs'))

    # Fails if Landmines aren't researched
    def test_unlock_trap_detection_fail(self):
        with self.assertRaises(LockedTechError) as e:
            self.avatar.get_tech_tree().player_functions.unlock_trap_detection()
        self.assertEqual(str(e.exception), 'Avatar must unlock Landmines before using Trap Detection.')

    # Tests that unlocking EMPs works
    def test_unlock_trap_detection(self):
        self.avatar.get_tech_tree().research('High Yield Drilling')
        self.avatar.get_tech_tree().research('Dynamite')
        self.avatar.get_tech_tree().research('Landmines')
        self.avatar.get_tech_tree().research('Trap Detection')
        self.assertTrue(self.avatar.is_researched('High Yield Drilling'))
        self.assertTrue(self.avatar.is_researched('Dynamite'))
        self.assertTrue(self.avatar.is_researched('Landmines'))
        self.assertTrue(self.avatar.is_researched('Trap Detection'))

    # Tests getting the researched techs
    def test_get_researched_techs(self):
        self.assertEqual(self.avatar.get_researched_techs(), ['Mining Robotics'])
        self.avatar.get_tech_tree().research('Better Drivetrains')
        self.assertEqual(self.avatar.get_researched_techs(), ['Mining Robotics', 'Better Drivetrains'])

    # Test the json with the new implementations
    def test_avatar_json(self):
        self.avatar.position = Vector(10, 10)
        data: dict = self.avatar.to_json()
        avatar: Avatar = Avatar().from_json(data)
        self.assertEqual(self.avatar.object_type, avatar.object_type)
        self.assertEqual(self.avatar.score, avatar.score)
        self.assertEqual(self.avatar.held_item, avatar.held_item)
        self.assertEqual(str(self.avatar.position), str(avatar.position))
        self.assertEqual(self.avatar.inventory, avatar.inventory)
        self.assertEqual(self.avatar.max_inventory_size, avatar.max_inventory_size)
        self.assertEqual(self.avatar.held_item, avatar.held_item)
        self.assertEqual(self.avatar.movement_speed, avatar.movement_speed)
        self.assertEqual(self.avatar.drop_rate, avatar.drop_rate)
        self.test_tech_tree()

    # helper method that checks a tech tree
    def test_tech_tree(self):
        other_tree: dict = self.avatar.get_tech_tree().to_json()
        for tech in self.avatar.get_tech_tree().tech_names():
            self.assertEqual(other_tree[tech], self.avatar.get_tech_tree().is_researched(tech))
        self.assertEqual(self.avatar.get_tech_tree().player_functions, other_tree['player_functions'])
