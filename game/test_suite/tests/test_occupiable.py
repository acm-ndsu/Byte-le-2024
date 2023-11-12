import unittest

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.occupiable import Occupiable
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.station.ore_occupiable_stations import *
from game.quarry_rush.station.ancient_tech_occupiable_station import AncientTechOccupiableStation
from game.utils.vector import Vector


class TestOccupiable(unittest.TestCase):
    def setUp(self) -> None:
        self.ore_station: OreOccupiableStation = OreOccupiableStation()

        self.locations: dict = {
            (Vector(1, 0),): [LambdiumOccupiableStation(),
                              CopiumOccupiableStation(),
                              TuriteOccupiableStation(),
                              ]}
        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)  # create 3x3 gameboard
        self.avatar = Avatar(position=Vector(1, 1))
        self.game_board.generate_map()

    def test_search_by_occupiable_object_type(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(ObjectType.LAMBDIUM_OCCUPIABLE_STATION),
                           LambdiumOccupiableStation))

    def test_search_by_occupiable_by_game_object(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(TuriteOccupiableStation()),
                           TuriteOccupiableStation))

    def test_search_by_occupiable_object_type_not_present(self):
        self.assertTrue(self.game_board.game_map[0][1].get_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION) is None)

    def test_search_by_occupiable_by_game_object_not_present(self):
        self.assertTrue(self.game_board.game_map[0][1].get_occupied_by(AncientTechOccupiableStation()) is None)

    def test_search_by_occupiable_by_game_object_general(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(OccupiableStation()),
                           OccupiableStation))

    # test is_occupied_by_object_type
    def test_is_occupied_by_object_type(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # ensure everything is on top of copium, and copium is not on top of itself
        self.assertTrue(copium_station.is_occupied_by_object_type(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertTrue(copium_station.is_occupied_by_object_type(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(copium_station.is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION))

        # ensure lambdium is only occupied by turite and nothing else
        self.assertFalse(lambdium_station.is_occupied_by_object_type(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertTrue(lambdium_station.is_occupied_by_object_type(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(lambdium_station.is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION))

        # ensure turite is occupied by nothing
        self.assertFalse(turite_station.is_occupied_by_object_type(ObjectType.LAMBDIUM_OCCUPIABLE_STATION))
        self.assertFalse(turite_station.is_occupied_by_object_type(ObjectType.TURITE_OCCUPIABLE_STATION))
        self.assertFalse(turite_station.is_occupied_by_object_type(ObjectType.COPIUM_OCCUPIABLE_STATION))

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

    # test is_occupied_by_game_object
    def test_is_occupied_by_game_object(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # ensure everything is on top of copium, and copium is not on top of itself
        self.assertTrue(copium_station.is_occupied_by_game_object(LambdiumOccupiableStation))
        self.assertTrue(copium_station.is_occupied_by_game_object(TuriteOccupiableStation))
        self.assertFalse(copium_station.is_occupied_by_game_object(CopiumOccupiableStation))

        # ensure lambdium is only occupied by turite and nothing else
        self.assertFalse(lambdium_station.is_occupied_by_game_object(LambdiumOccupiableStation))
        self.assertTrue(lambdium_station.is_occupied_by_game_object(TuriteOccupiableStation))
        self.assertFalse(lambdium_station.is_occupied_by_game_object(CopiumOccupiableStation))

        # ensure turite is occupied by nothing
        self.assertFalse(turite_station.is_occupied_by_game_object(LambdiumOccupiableStation))
        self.assertFalse(turite_station.is_occupied_by_game_object(TuriteOccupiableStation))
        self.assertFalse(turite_station.is_occupied_by_game_object(CopiumOccupiableStation))

    def test_remove_game_object_from_occupied_by(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        turite_station: TuriteOccupiableStation = TuriteOccupiableStation()

        # set occupied by order: copium -> lambdium -> turite
        lambdium_station.occupied_by = turite_station
        copium_station.occupied_by = lambdium_station

        # Test that removing turite works and that the stack is only copium -> turite
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(turite_station),
                         turite_station)
        self.assertEqual(copium_station.occupied_by, lambdium_station)
        self.assertEqual(lambdium_station.occupied_by, None)

    def test_remove_game_object_from_occupied_by_duplicates(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_1: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_2: LambdiumOccupiableStation = LambdiumOccupiableStation()

        # set occupied by order: copium -> lambdium -> lambdium1 -> lambdium2
        lambdium_station_1.occupied_by = lambdium_station_2
        lambdium_station.occupied_by = lambdium_station_1
        copium_station.occupied_by = lambdium_station

        # test the lambdium is removed in the order lambdium -> lambdium1 -> lambdium2
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station),
                         lambdium_station)
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station_1),
                         lambdium_station_1)
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station_2),
                         lambdium_station_2)
        self.assertEqual(copium_station.occupied_by, None)

    # test the method still works in any order
    def test_remove_game_object_from_occupied_by_out_of_order(self):
        copium_station: CopiumOccupiableStation = CopiumOccupiableStation()
        lambdium_station: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_1: LambdiumOccupiableStation = LambdiumOccupiableStation()
        lambdium_station_2: LambdiumOccupiableStation = LambdiumOccupiableStation()

        # set occupied by order: copium -> lambdium -> lambdium1 -> lambdium2
        lambdium_station_1.occupied_by = lambdium_station_2
        lambdium_station.occupied_by = lambdium_station_1
        copium_station.occupied_by = lambdium_station

        # test the lambdium is removed in the order lambdium2 -> lambdium -> lambdium1
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station_2),
                         lambdium_station_2)
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station),
                         lambdium_station)
        self.assertEqual(copium_station.remove_game_object_from_occupied_by(lambdium_station_1),
                         lambdium_station_1)
        self.assertEqual(copium_station.occupied_by, None)
