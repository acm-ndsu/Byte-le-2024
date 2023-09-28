from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.entity.ores import Ore, Lambdium, Turite, Copium
from game.quarry_rush.avatar.inventory_manager import InventoryManager


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds generic ore, inherits from OccupiableStation.

    This station is inherited by other ore occupiable stations.
    """

    def __init__(self, held_item: Ore | None = None):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager = None) -> Item | None:
        if InventoryManager is None:
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, avatar.company)
        self.held_item = None

        return None


class LambdiumOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Lambdium ore.
    """
    def __init__(self, held_item: Lambdium | None = Lambdium()):
        super().__init__(held_item=held_item)


class TuriteOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Turite ore.
    """
    def __init__(self, held_item: Turite | None = Turite()):
        super().__init__(held_item=held_item)


class CopiumOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Copium ore.
    """
    def __init__(self, held_item: Copium | None = Copium()):
        super().__init__(held_item=held_item)
