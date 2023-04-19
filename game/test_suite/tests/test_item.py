import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.enums import ObjectType

# class to test the item class and its methods
class TestItem(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, None, [], 1)
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
            self.item = Item(10, None, 10, 10)
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

    # test set quantity
    def test_set_quantity(self):
        self.item = Item(10, None, 10, 10)
        self.item.quantity = 5
        self.assertEqual(self.item.quantity, 5)

    def test_set_quantity_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = 'fail'
        self.assertEqual(str(e.exception), 'Item.quantity must be an int.')

    def test_set_quantity_fail_greater_than_0(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = 0
        self.assertEqual(str(e.exception), 'Item.quantity must be greater than 0.')

    def test_set_quantity_fail_stack_size(self):
        with self.assertRaises(ValueError) as e:
            self.item.quantity = 10
            self.item.stack_size = 1
        self.assertEqual(str(e.exception), 'Item.quantity cannot be greater than Item.stack_size')

    def test_stack_size(self):
        self.item = Item(10, None, 10, 10)
        self.assertEqual(self.item.quantity, 10)

    def test_stack_size_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.stack_size = 'fail'
        self.assertEqual(str(e.exception), 'Item.stack_size must be an int.')

    def test_stack_size_fail_quantity(self):
        # value, durability, quantity, stack size
        with self.assertRaises(ValueError) as e:
            item: Item = Item(10, None, 10, 10)
            item.stack_size = 5
        self.assertEqual(str(e.exception), 'Item.stack_size must be greater than or equal to the quantity.')

    def test_pick_up(self):
        # value, durability, quantity, stack size
        item: Item = Item(10, None, 2, 10)
        self.item = Item(10, None, 1, 10)
        self.item.pick_up(item)
        self.assertEqual(self.item.quantity, 3)

    def test_pick_up_fail(self):
        with self.assertRaises(ValueError) as e:
            self.item.pick_up(self.item.pick_up(None))
        self.assertEqual(str(e.exception), 'NoneType is not of type Item.')

    def test_pick_up_wrong_object_type(self):
        item: Item = Item(10, 10, 1, 1)
        item.object_type = ObjectType.PLAYER
        self.item = Item(10, 10, 1, 1)
        self.item = self.item.pick_up(item)
        self.assertEqual(self.item.object_type, item.object_type)

    def test_pick_up_surplus(self):
        item: Item = Item(10, None, 10, 10)
        self.item = Item(10, None, 9, 10)
        surplus: Item = self.item.pick_up(item)
        self.assertEqual(surplus.quantity, 9)

    def test_item_json(self):
        data: dict = self.item.to_json()
        item: Item = Item().from_json(data)
        self.assertEqual(self.item.object_type, item.object_type)
        self.assertEqual(self.item.value, item.value)
        self.assertEqual(self.item.stack_size, item.stack_size)
        self.assertEqual(self.item.durability, item.durability)
        self.assertEqual(self.item.quantity, item.quantity)