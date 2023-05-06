from game.common.avatar import Avatar
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.game_object import GameObject
from typing import Self


# create station object that contains occupied_by
class OccupiableStation(Occupiable, Station):
    """
    Occupiable Stations are stations that can have things in them, including the player. These can be created to have
    items the player can take, or it can be occupied by any other GameObject.
    """
    def __init__(self, held_item: Item | None = None, occupied_by: GameObject | None = None):
        super().__init__(occupied_by=occupied_by, held_item=held_item)
        self.object_type: ObjectType = ObjectType.OCCUPIABLE_STATION
        self.held_item = held_item
        self.occupied_by = occupied_by

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        occupied_by = data['occupied_by']
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
            case _:
                raise Exception(f'Could not parse occupied_by: {occupied_by}')
        return self
