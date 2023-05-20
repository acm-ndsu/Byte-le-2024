from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station


# create example of station that takes held_item from avatar at inventory slot 0
class StationReceiverExample(Station):
    def __init__(self, held_item: Item | None = None):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.STATION_RECEIVER_EXAMPLE

    def take_action(self, avatar: Avatar) -> None:
        self.held_item = avatar.drop_held_item()
