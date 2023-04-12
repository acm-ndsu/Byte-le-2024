from game.common.avatar import Avatar
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.game_object import GameObject
from typing import Self

# create station object that contains occupied_by
class Occupiable_Station(Occupiable, Station):
    def __init__(self, item: Item = None, occupied_by: GameObject = None):
        super().__init__(occupied_by=occupied_by, item=item)
        self.object_type: ObjectType = ObjectType.OCCUPIABLE_STATION

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        # Add all possible game objects that can occupy a tile here (requires python 3.10) 
        match occupied_by['object_type']:
            case ObjectType.AVATAR:
                self.occupied_by: Avatar = Avatar().from_json(data['occupied_by'])
            case ObjectType.OCCUPIABLE_STATION:
                self.occupied_by: Occupiable_Station = Occupiable_Station().from_json(data['occupied_by'])
            case ObjectType.STATION:
                self.occupied_by: Station = Station().from_json(data['occupied_by'])
            case _:
                raise Exception(f'Could not parse occupied_by: {self.occupied_by}')                  
        return self

        