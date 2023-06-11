import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.utils.vector import Vector
from game.common.enums import ObjectType


class TestItem(unittest.TestCase):
    """
    This class is to test the Item class and its methods.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, 1)
        self.item: Item = Item()

    # test set durability
    def test_set_durability(self):
        self.item.durability = 10
        self.assertEqual(self.item.durability, 10)

    def test_set_durability_none(self):
        self.item.durability = None
        self.assertEqual(self.item.durability, None)

    def test_set_durability_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.durability = 'fail'
        self.assertEqual(str(e.exception), 'Item.durability must be an int or None.')

    def test_set_durability_stack_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item = Item(10, 10, None, 10, 10)
            self.item.durability = 19
        self.assertEqual(str(e.exception), 'Item.durability must be set to None if stack_size is not equal to 1.')

    # test set value
    def test_set_value(self):
        self.item.value = 10
        self.assertEqual(self.item.value, 10)

    def test_set_value_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.value = 'fail'
        self.assertEqual(str(e.exception), 'Item.value must be an int.')
    def test_set_science_point_value(self):
        self.item.science_point_value = 10
        self.assertEqual(self.item.science_point_value, 10)

    def test_set_science_point_value_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.science_point_value = 'fail'
        self.assertEqual(str(e.exception), 'Item.science_point_value must be an int.')
    # test set quantity
    def test_set_quantity(self):
        self.item = Item(10, 10, None, 10, 10)
        self.item.quantity = 5
        self.assertEqual(self.item.quantity, 5)

    def test_set_quantity_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = 'fail'
        self.assertEqual(str(e.exception), 'Item.quantity must be an int.')

    def test_set_quantity_fail_greater_than_0(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = -1
        self.assertEqual(str(e.exception), 'Item.quantity must be greater than or equal to 0.')

    def test_set_quantity_fail_stack_size(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = 10
            self.item.stack_size = 1
        self.assertEqual(str(e.exception), 'Item.quantity cannot be greater than Item.stack_size')

    # test set stack_size
    def test_set_stack_size(self):
        self.item = Item(10, 10, None, 10, 10)
        self.assertEqual(self.item.quantity, 10)

    def test_set_stack_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.stack_size = 'fail'
        self.assertEqual(str(e.exception), 'Item.stack_size must be an int.')

    def test_set_stack_size_fail_quantity(self):
        # value, durability, quantity, stack size
        with self.assertRaises(ValueError) as e:
            item: Item = Item(10,10, None, 10, 10)
            item.stack_size = 5
        self.assertEqual(str(e.exception), 'Item.stack_size must be greater than or equal to the quantity.')

    # test set position
    def test_set_position(self):
        self.position = Vector(2, 2)
        self.item.position = self.position
        self.assertEqual(self.item.position.object_type, self.position.object_type)
        self.assertEqual(self.item.position.x, self.position.x)
        self.assertEqual(self.item.position.y, self.position.y)

    def test_set_position_none(self):
        self.position = None
        self.assertEqual(self.item.position, None)

    def test_set_position_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.position = "Not accepted"
        self.assertEqual(str(e.exception), 'Item.position must be a Vector or None.')

    # test set name
    def test_set_name(self):
        self.item.name = 'Test Name'
        self.assertEqual(self.item.name, 'Test Name')   

    def test_set_name_none(self):
        self.item.name = None
        self.assertEqual(self.item.name, None)

    def test_name_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.name = Vector(3, 2)
        self.assertEqual(str(e.exception), 'Item.name must be a str or None.')

    def test_pick_up(self):
        # value, durability, quantity, stack size
        item: Item = Item(10, 10, None, 2, 10)
        self.item = Item(10,10, None, 1, 10)
        self.item.pick_up(item)
        self.assertEqual(self.item.quantity, 3)

    def test_pick_up_wrong_object_type(self):
        item: Item = Item(10, 10, 10, 1, 1)
        item.object_type = ObjectType.PLAYER
        self.item = Item(10,  10, 10, 1, 1)
        self.item = self.item.pick_up(item)
        self.assertEqual(self.item.object_type, item.object_type)

    def test_pick_up_surplus(self):
        item: Item = Item(10, 10, None, 10, 10)
        self.item = Item(10, 10, None, 9, 10)
        surplus: Item = self.item.pick_up(item)
        self.assertEqual(surplus.quantity, 9)

    def test_item_json(self):
        self.item.position = Vector(2, 2)
        self.item.name = "Test"
        data: dict = self.item.to_json()
        item: Item = Item().from_json(data)
        self.assertEqual(self.item.object_type, item.object_type)
        self.assertEqual(self.item.value, item.value)
        self.assertEqual(self.item.stack_size, item.stack_size)
        self.assertEqual(self.item.durability, item.durability)
        self.assertEqual(self.item.quantity, item.quantity)
        self.assertEqual(self.item.science_point_value, item.science_point_value)
        self.assertEqual(self.item.position.object_type, item.position.object_type)
        self.assertEqual(self.item.position.x, item.position.x)
        self.assertEqual(self.item.position.y, item.position.y)
        self.assertEqual(self.item.name, item.name)
