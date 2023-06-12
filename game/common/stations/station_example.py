from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station


# create example of station that gives item to avatar
class StationExample(Station):
    def __init__(self, held_item: Item | None = None):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.STATION_EXAMPLE

    def take_action(self, avatar: Avatar) -> Item | None:
        pass
        avatar.pick_up(self.held_item)
