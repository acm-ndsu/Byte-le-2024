import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
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

    # test set inventory
    def test_avatar_set_inventory(self):
        self.avatar.inventory = [Item(1, 1)]
        self.assertEqual(self.avatar.inventory[0].value, Item(1, 1).value)

    # fails if inventory is not a list
    def test_avatar_set_inventory_fail_1(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.inventory must be a list of Items.')

    # fails if inventory size is greater than the max_inventory_size
    def test_avatar_set_inventory_fail_2(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = [Item(1, 1), Item(4, 2)]
        self.assertEqual(str(e.exception), 'Avatar.inventory size must be less than or equal to max_inventory_size')

    def test_avatar_set_max_inventory_size(self):
        self.avatar.max_inventory_size = 10
        self.assertEqual(str(self.avatar.max_inventory_size), str(10))

    def test_avatar_set_max_inventory_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.avatar.max_inventory_size = 'Fail'
        self.assertEqual(str(e.exception), 'Avatar.max_inventory_size must be an int.')

    # Tests picking up an item
    def test_avatar_pick_up(self):
        self.avatar.pick_up(self.item)
        self.assertEqual(self.avatar.inventory[0], self.item)

    # Tests that picking up an item successfully returns None
    def test_avatar_pick_up_return_none(self):
        returned: Item | None = self.avatar.pick_up(self.item)
        self.assertEqual(returned, None)

    # Tests that picking up an item of one that already exists in the inventory works
    def test_avatar_pick_up_extra(self):
        self.item1: Item = Item(10, 0, 1, 3)
        self.item2: Item = Item(10, 0, 1, 3)
        self.item3: Item = Item(10, 0, 1, 3)
        self.avatar.pick_up(self.item1)
        self.avatar.pick_up(self.item2)
        self.avatar.pick_up(self.item3)
        self.assertEqual(self.avatar.held_item.quantity, 3)

    # Tests when an item is being taken away
    def test_take(self):
        self.avatar: Avatar = Avatar(None, 3)
        self.avatar.inventory = [Item(quantity=5, stack_size=5), Item(quantity=7, stack_size=7),
                                 Item(quantity=10, stack_size=10)]
        taken = self.avatar.take(Item(quantity=3, stack_size=3))

        self.assertEqual(taken, None)

        """
        When this test is performed, it works properly, but because the Item class is used and is very generic, it 
        may not seem to be the case. However, it does work in the end. The first item in the inventory has its 
        quantity decrease to 2 after the take method is executed. Then, the helper method, clean_inventory, 
        consolidates all similar Items with each other. This means that inventory[1] will add its quantity to 
        inventory[0], making it have a quantity of 5; inventory[1] now has a quantity of 4 instead of 7. Then, 
        inventory[3] will add its quantity to inventory[1], making it have a quantity of 7; inventory[3] now has a 
        quantity of 7 too. 
        
        TL;DR
        When the take method is used, it will work properly with more specific Item classes being created to 
        consolidate the same Item object types together
        """
        self.assertEqual(self.avatar.inventory[2].quantity, 7)

    # Tests when the None value is being taken away
    def test_take_none(self):
        taken = self.avatar.take(None)
        self.assertEqual(taken, None)

    def test_take_fail(self):
        self.avatar: Avatar = Avatar(None, 3)
        self.avatar.inventory = [Item(quantity=5, stack_size=5), Item(quantity=7, stack_size=7),
                                 Item(quantity=10, stack_size=10)]
        with self.assertRaises(ValueError) as e:
            taken = self.avatar.take('')
        self.assertEqual(str(e.exception), 'str is not of type Item.')

    # Tests picking up an item and failing
    def test_avatar_pick_up_full_inventory(self):
        self.avatar.pick_up(self.item)

        # Pick up again to test
        returned: Item | None = self.avatar.pick_up(self.item)
        self.assertEqual(returned, self.item)

    # Tests dropping the held item
    def test_avatar_drop_held_item(self):
        self.avatar.pick_up(self.item)
        held_item = self.avatar.drop_held_item()
        self.assertEqual(held_item, self.item)

    def test_avatar_drop_held_item_none(self):
        held_item = self.avatar.drop_held_item()
        self.assertEqual(held_item, None)

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
