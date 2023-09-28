from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.entity.ores import Ore
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class OreOccupiableStation(OccupiableStation):
    # MAKE 4 STATION CLASSES FOR EACH ORE OBJECT. THE TAKE ACTION METHOD WON'T CHANGE

    def __init__(self, held_item: Ore | None = None):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager = None) -> Item | None:
        if InventoryManager is None:
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, avatar.company)
        self.held_item = None

        return None
