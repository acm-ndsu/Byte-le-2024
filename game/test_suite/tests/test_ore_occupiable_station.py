import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from game.common.stations.station import Station
from game.quarry_rush.station.ore_occupiable_stations import OreOccupiableStation


class TestOreOccupiableStation(unittest.TestCase):
    def setUp(self) -> None:
        self.ore_station: OreOccupiableStation = OreOccupiableStation()

        self.locations: dict = {
            (Vector(1, 0), Vector(2, 0), Vector(0, 1), Vector(0, 2)): [OreOccupiableStation(None),
                                                                       OreOccupiableStation(None),
                                                                       OreOccupiableStation(None),
                                                                       OreOccupiableStation(None)]}
        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)  # create 3x3 gameboard
        self.avatar = Avatar(position=Vector(1, 1))
        self.game_board.generate_map()

