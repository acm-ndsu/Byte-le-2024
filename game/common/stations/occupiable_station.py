from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.game_object import GameObject
from game.common.map.tile import Tile
from typing import Self

# create station object that contains occupied_by
class Occupiable_Station(Tile, Station):
    def __init__(self, item: Item = None, occupied_by: GameObject = None):
        super().__init__(occupied_by=occupied_by, item=item)
        self.object_type: ObjectType = ObjectType.OCCUPIABLE_STATION

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        return data
    
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        return self

        