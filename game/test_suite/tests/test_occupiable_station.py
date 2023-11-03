import unittest

from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.quarry_rush.station.ore_occupiable_stations import *


class TestOccupiableStation(unittest.TestCase):
    """
    `Test Item Notes:`

        This class tests the different methods in the OccupiableStation class and ensures the objects that occupy them
        are properly set.
    """

    def setUp(self) -> None:
        self.occupiable_station: OccupiableStation = OccupiableStation()
        self.occupiable_station1: OccupiableStation = OccupiableStation()
        self.wall: Wall = Wall()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()
        self.item: Item = Item()

    # test adding wall to occupiable_station
    def test_wall_occ(self):
        self.occupiable_station.occupied_by = self.wall
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.WALL)

    # test adding station to occupiable_station
    def test_station_occ(self):
        self.occupiable_station.occupied_by = self.station
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.STATION)

    # test adding avatar to occupiable_station
    def test_avatar_occ(self):
        self.occupiable_station.occupied_by = self.avatar
        self.assertEqual(self.occupiable_station.occupied_by.object_type, ObjectType.AVATAR)

    # test adding item to occupiable_station
    def test_item_occ(self):
        self.occupiable_station.item = self.item
        self.assertEqual(self.occupiable_station.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.occupiable_station.item.durability, self.item.durability)
        self.assertEqual(self.occupiable_station.item.value, self.item.value)

    # test cannot add item to occupied_by
    def test_fail_item_occ(self):
        with self.assertRaises(ValueError) as e:
            self.occupiable_station.occupied_by = self.item
        self.assertEqual(str(e.exception), 'OccupiableStation.occupied_by cannot be an Item.')

    # test is_occupied_by_method
    def test_is_occupied_by_method(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # ensure everything is on top of copium, and copium is not on top of itself
        self.assertTrue(copium_station.is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertTrue(copium_station.is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(copium_station.is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        # ensure lambdium is only occupied by turite and nothing else
        self.assertFalse(lambdium_station.is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertTrue(lambdium_station.is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(lambdium_station.is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

        # ensure turite is occupied by nothing
        self.assertFalse(turite_station.is_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertFalse(turite_station.is_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(turite_station.is_occupied_by(ObjectType.COPIUM_OCCUPIABLE_STATION))

    # test removing an object from an occupied_by stack of size 2
    def test_remove_from_occupied_by_2_stack(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()

        # set occupied by order: copium -> lambdium
        copium_station.occupied_by = lambdium_station

        # Test that removing lambdium works
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                         lambdium_station)

    # test removing an object from an occupied_by stack twice
    def test_remove_from_occupied_by_twice(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # Test that removing lambdium works and that trying to remove it again returns None
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                         lambdium_station)
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION), None)

    # test removing an object from the top of the stack
    def test_remove_from_occupied_by_top_object(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # Test that removing turite works and that the stack is only copium -> turite
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.TURITE_OCCUPIABLE_STATION),
                         turite_station)
        self.assertEqual(copium_station.occupied_by, lambdium_station)
        self.assertEqual(lambdium_station.occupied_by, None)

    # test removing duplicate objects in the stack
    def test_remove_from_occupied_by_duplicates(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_1: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_2: LambdiumOccupiableStation = LambdiumOccupiableStation()

        # set occupied by order: copium -> lambdium -> lambdium1 -> lambdium2
        lambdium_station_1.occupied_by = lambdium_station_2
        lambdium_station.occupied_by = lambdium_station_1
        copium_station.occupied_by = lambdium_station

        # test the lambdium is removed in the order lambdium -> lambdium1 -> lambdium2
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                         lambdium_station)
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                         lambdium_station_1)
        self.assertEqual(copium_station.remove_from_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                         lambdium_station_2)
        self.assertEqual(copium_station.occupied_by, None)

    # test json method
    def test_occ_json(self):
        self.occupiable_station.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: OccupiableStation = OccupiableStation().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)

    # test json method with nested occupiable_station
    def test_nested_occ_json(self):
        self.occupiable_station.occupied_by = self.occupiable_station1
        self.occupiable_station.occupied_by.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: OccupiableStation = OccupiableStation().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
        self.assertEqual(self.occupiable_station.occupied_by.object_type, occupiable_station.occupied_by.object_type)
        assert (isinstance(occupiable_station.occupied_by, OccupiableStation))
        self.assertEqual(self.occupiable_station.occupied_by.occupied_by.object_type,
                         occupiable_station.occupied_by.occupied_by.object_type)
