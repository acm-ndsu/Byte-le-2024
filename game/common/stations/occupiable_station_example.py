from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.occupiable_station import OccupiableStation

# create example of occupiable_station that gives item 
class OccupiableStationExample(OccupiableStation):
    def __init__(self, held_item: Item | None = None):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.STATION_EXAMPLE
    
    def take_action(self, avatar: Avatar) -> Item | None:
        avatar.pick_up(self.held_item)