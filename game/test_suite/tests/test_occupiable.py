import unittest

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation
from game.utils.vector import Vector


class TestOccupiable(unittest.TestCase):
    def setUp(self) -> None:
        self.ore_station: OreOccupiableStation = OreOccupiableStation()
        self.avatar = Avatar(position=Vector(1, 1))

        # adds ores to all adjacent tiles and the one the avatar will be on
        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            (Vector(1, 0), Vector(1, 0)): [self.ore_station, self.avatar]}

        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)  # create 3x3 gameboard
        self.game_board.generate_map()

    def test_search_by_occupiable_object_type(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(ObjectType.AVATAR),
                                   Avatar))

    def test_search_by_occupiable_by_game_object(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(OreOccupiableStation()),
                                   OreOccupiableStation))

    def test_search_by_occupiable_object_type_not_present(self):
        self.assertTrue(
            self.game_board.game_map[0][1].get_occupied_by(ObjectType.ANCIENT_TECH_OCCUPIABLE_STATION) is None)

    def test_search_by_occupiable_by_game_object_general(self):
        self.assertTrue(isinstance(self.game_board.game_map[0][1].get_occupied_by(OccupiableStation()),
                                   OccupiableStation))

    # test is_occupied_by_object_type
    def test_is_occupied_by_object_type(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()

        # set occupied by order: ore occupiable station -> dynamite -> avatar
        ore_station.occupied_by = Dynamite()
        ore_station.occupied_by.occupied_by = self.avatar

        # ensure everything is on top of ore station and it is not on top of itself
        self.assertTrue(ore_station.is_occupied_by_object_type(ObjectType.DYNAMITE))
        self.assertTrue(ore_station.is_occupied_by_object_type(ObjectType.AVATAR))
        self.assertFalse(ore_station.is_occupied_by_object_type(ObjectType.ORE_OCCUPIABLE_STATION))

    # test removing an object from an occupied_by stack of size 2
    def test_remove_from_occupied_by_2_stack(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        dynamite: Dynamite = Dynamite()

        # set occupied by order: ore station -> dynamite
        ore_station.occupied_by = dynamite

        # Test that removing dynamite works
        self.assertTrue(isinstance(ore_station.remove_from_occupied_by(ObjectType.DYNAMITE), Dynamite))

    # test removing an object from an occupied_by stack twice
    def test_remove_from_occupied_by_twice(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        ore_station_1: OreOccupiableStation = OreOccupiableStation()

        # set occupied by order: ore station -> ore station 1
        ore_station.occupied_by = ore_station_1

        # Test that removing ore works and that trying to remove it again returns None
        self.assertEqual(ore_station.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION),
                         ore_station_1)
        self.assertEqual(ore_station.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION), None)

    # test removing duplicate objects in the stack
    def test_remove_from_occupied_by_duplicates(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        ore_station_1: OreOccupiableStation = OreOccupiableStation()
        ore_station_2: OreOccupiableStation = OreOccupiableStation()
        ore_station_3: OreOccupiableStation = OreOccupiableStation()

        # set occupied by order: ore station -> ore station 1 -> ore station 2 -> ore station 3
        ore_station.occupied_by = ore_station_1
        ore_station_1.occupied_by = ore_station_2
        ore_station_2.occupied_by = ore_station_3

        # test the stations are removed in the order: ore station 1 -> ore station 2 -> ore station 3
        self.assertEqual(ore_station.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION),
                         ore_station_1)
        self.assertEqual(ore_station.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION),
                         ore_station_2)
        self.assertEqual(ore_station.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION),
                         ore_station_3)
        self.assertEqual(ore_station.occupied_by, None)

    # test is_occupied_by_game_object
    def test_is_occupied_by_game_object(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        dynamite: Dynamite = Dynamite()

        # set occupied by order: ore station -> dynamite
        ore_station.occupied_by = dynamite

        self.assertTrue(ore_station.is_occupied_by_game_object(Dynamite))

    def test_remove_game_object_from_occupied_by(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        dynamite: Dynamite = Dynamite()

        # set occupied by order: ore station -> dynamite
        ore_station.occupied_by = dynamite

        # Test that removing turite works and that the stack is only copium -> turite
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(dynamite),
                         dynamite)
        self.assertEqual(ore_station.occupied_by, None)

    def test_remove_game_object_from_occupied_by_duplicates(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        ore_station_1: OreOccupiableStation = OreOccupiableStation()
        ore_station_2: OreOccupiableStation = OreOccupiableStation()
        ore_station_3: OreOccupiableStation = OreOccupiableStation()

        # set occupied by order: ore station -> ore station 1 -> ore station 2 -> ore station 3
        ore_station.occupied_by = ore_station_1
        ore_station_1.occupied_by = ore_station_2
        ore_station_2.occupied_by = ore_station_3

        # test the stations are removed in the order: ore station 1 -> ore station 2 -> ore station 3
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_1),
                         ore_station_1)
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_2),
                         ore_station_2)
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_3),
                         ore_station_3)
        self.assertEqual(ore_station.occupied_by, None)

    # test the method still works in any order
    def test_remove_game_object_from_occupied_by_out_of_order(self):
        ore_station: OreOccupiableStation = OreOccupiableStation()
        ore_station_1: OreOccupiableStation = OreOccupiableStation()
        ore_station_2: OreOccupiableStation = OreOccupiableStation()
        ore_station_3: OreOccupiableStation = OreOccupiableStation()

        # set occupied by order: ore station -> ore station 1 -> ore station 2 -> ore station 3
        ore_station.occupied_by = ore_station_1
        ore_station_1.occupied_by = ore_station_2
        ore_station_2.occupied_by = ore_station_3

        # test the stations are removed in the order: ore station 2 -> ore station 3 -> ore station 1
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_2),
                         ore_station_2)
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_3),
                         ore_station_3)
        self.assertEqual(ore_station.remove_game_object_from_occupied_by(ore_station_1),
                         ore_station_1)
        self.assertEqual(ore_station.occupied_by, None)
