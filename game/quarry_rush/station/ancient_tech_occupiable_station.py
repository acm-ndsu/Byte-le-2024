from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class AncientTechOccupiableStation(OccupiableStation):
    """
    Station that holds ancient tech, inherits from OccupiableStation.
    """

    def __init__(self, held_item: AncientTech = AncientTech()):
        super().__init__(held_item=held_item)

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager) -> None:
        if InventoryManager is None:
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, avatar.company)
        self.held_item = None
