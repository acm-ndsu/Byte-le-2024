from typing import Self

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.common.map.occupiable import Occupiable
from game.common.stations.station import Station


# create station object that contains occupied_by
class OccupiableStation(Occupiable, Station):
    """
    `OccupiableStation Class Notes:`

        Occupiable Station objects inherit from both the Occupiable and Station classes. This allows for other objects to
        be "on top" of the Occupiable Station. For example, an Avatar object can be on top of this object. Since Stations
        can contain items, items can be stored in this object too.

        Any GameObject or Item can be in an Occupiable Station.

        Occupiable Station Example is a small file that shows an example of how this class can be
        used. The example class can be deleted or expanded upon if necessary.
    """

    def __init__(self, held_item: Item | None = None, occupied_by: GameObject | None = None):
        super().__init__(occupied_by=occupied_by, held_item=held_item)
        self.object_type: ObjectType = ObjectType.OCCUPIABLE_STATION
        self.held_item = held_item
        self.occupied_by = occupied_by

    def from_json(self, data: dict) -> Self:
        from game.quarry_rush.station.ore_occupiable_station import OreOccupiableStation

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
            case ObjectType.ORE_OCCUPIABLE_STATION:
                self.occupied_by: OreOccupiableStation = OreOccupiableStation().from_json(occupied_by)
            case ObjectType.STATION:
                self.occupied_by: Station = Station().from_json(occupied_by)
            case _:
                self.occupied_by = None
        return self
