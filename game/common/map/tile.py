from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.stations.occupiable_station import Occupiable_Station
from game.common.stations.station import Station
from typing import Self

"""This object exists to encapsulate all objects that could be placed on the gameboard"""
class Tile(GameObject):
    def __init__(self, occupied_by: GameObject = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.TILE
        self.occupied_by: GameObject|None = occupied_by


    @property
    def occupied_by(self) -> GameObject|None:
        return self.__occupied_by

    @occupied_by.setter
    def occupied_by(self, occupied_by: GameObject|None) -> None:
        if occupied_by is not None and not isinstance(occupied_by, GameObject):
            raise ValueError(f'{self.__class__.__name__}.occupied_by must be None or an instance of GameObject.')
        self.__occupied_by = occupied_by  

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['occupied_by'] = self.occupied_by.to_json() if self.occupied_by is not None else None
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by: GameObject|None = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        
        # Add all possible game objects that can occupy a tile here (requires python 3.10) 
        match occupied_by['object_type']:
            case ObjectType.AVATAR:
                self.occupied_by = Avatar().from_json(data['occupied_by'])
            case ObjectType.OCCUPIABLE_STATION:
                self.occupied_by = Occupiable_Station().from_json(data['occupied_by'])
            case ObjectType.STATION:
                self.occupied_by = Station().from_json(data['occupied_by'])
            case _:
                raise Exception(f'Could not parse occupied_by: {self.occupied_by}')                  
        return self