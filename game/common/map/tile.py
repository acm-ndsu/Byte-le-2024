from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.stations.station import Station
from typing import Self

"""This object exists to encapsulate all objects that could be placed on the gameboard"""
class Tile(GameObject):
    def __init__(self, occupied_by: GameObject = None):
        super().__init__()
        self.object_type = ObjectType.TILE
        self.occupied_by = occupied_by


    @property
    def occupied_by(self) -> GameObject:
        return self.__occupied_by

    @occupied_by.setter
    def occupied_by(self, occupied_by: GameObject):
        if isinstance(occupied_by, GameObject):
            self.__occupied_by = occupied_by  
        else:
            self.__occupied_by = None 

    def to_json(self):
        data = super().to_json()
        data['occupied_by'] = self.occupied_by.to_json() if self.occupied_by else None
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by = data['occupied_by']
        if not occupied_by:
            return self
        
        # Add all possible game objects that can occupy a tile here (requires python 3.10) 
        match occupied_by["object_type"]:
            case ObjectType.AVATAR:
                self.occupied_by = Avatar().from_json(data['occupied_by'])
            case ObjectType.OCCUPIABLE_STATION:
                self.occupied_by = Occupiable_Station().from_json(data['occupied_by'])
            case ObjectType.STATION:
                self.occupied_by = Station().from_json(data['occupied_by'])
            case _:
                raise Exception(f'Could not parse occupied_by: {self.occupied_by}')                  
        return self