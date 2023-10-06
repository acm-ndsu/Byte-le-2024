from json import load
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.wall import Wall
from game.quarry_rush.station.company_station import ChurchStation, TuringStation
from game.common.enums import Company


class GameLocation:
    """
    GameLocation opens the game_location.json and maps its values to the appropriate stations.
    This file is for generating set values for the map, not random locations, this includes:
        - walls (not including the border)
        - turing_bases
        - church_bases
    """
    def __init__(self):
        f = open('game/quarry_rush/map/game_location/game_location.json')
        game_location: dict = load(f)
        f.close()

        self.__walls: dict = game_location['walls']
        self.__turing_bases: dict = game_location['turing_bases']
        self.__church_bases: dict = game_location['church_bases']

    def generate_location(self) -> dict[tuple[Vector]: list[GameObject]]:
        game_location: dict = {}
        for pos in self.__walls:
            game_location[(Vector(x=pos[0], y=pos[1]),)] = [Wall(), ]
        for pos in self.__turing_bases:
            game_location[(Vector(x=pos[0], y=pos[1]),)] = [TuringStation(), ]
        for pos in self.__church_bases:
            game_location[(Vector(x=pos[0], y=pos[1]),)] = [ChurchStation(), ]

        return game_location
