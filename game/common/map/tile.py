from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.station import Station
from game.common.map.wall import Wall
from typing import Self


class Tile(Occupiable):
    """
    This object exists to encapsulate all objects that could be placed on the gameboard.

    Tiles will represent things like the floor in the game. They inherit from Occupiable, which allows for tiles to
    have certain GameObjects and the avatar in it.
    """
    def __init__(self, occupied_by: GameObject = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.TILE

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by: dict | None = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        # Add all possible game objects that can occupy a tile here (requires python 3.10) 
        match ObjectType(occupied_by['object_type']):
            case ObjectType.AVATAR:
                self.occupied_by: Avatar = Avatar().from_json(occupied_by)
            case ObjectType.OCCUPIABLE_STATION:
                self.occupied_by: OccupiableStation = OccupiableStation().from_json(occupied_by)
            case ObjectType.STATION:
                self.occupied_by: Station = Station().from_json(occupied_by)
            case ObjectType.WALL:
                self.occupied_by: Wall = Wall().from_json(occupied_by)
            case _:
                raise Exception(f'Could not parse occupied_by: {occupied_by}')                  
        return self