from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ores import Ore, Lambdium, Turite, Copium


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds generic ore, inherits from OccupiableStation.

    This station is inherited by other ore occupiable stations.
    """

    def __init__(self, held_item: Ore = Ore()):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager = None) -> None:
        if InventoryManager is None:
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, avatar.company)
        self.held_item = None


class LambdiumOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Lambdium ore.
    """

    def __init__(self, held_item: Lambdium = Lambdium()):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.LAMBDIUM_OCCUPIABLE_STATION


class TuriteOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Turite ore.
    """

    def __init__(self, held_item: Turite = Turite()):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.TURITE_OCCUPIABLE_STATION


class CopiumOccupiableStation(OreOccupiableStation):
    """
    Occupiable Station that holds Copium ore.
    """

    def __init__(self, held_item: Copium = Copium()):
        super().__init__(held_item=held_item)
        self.object_type = ObjectType.COPIUM_OCCUPIABLE_STATION
