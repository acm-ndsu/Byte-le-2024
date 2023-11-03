import unittest

from game.common.avatar import Avatar
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
