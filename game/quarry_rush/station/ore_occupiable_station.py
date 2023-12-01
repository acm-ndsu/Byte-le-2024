import random
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.entity.ores import Lambdium, Turite, Copium
from game.utils.vector import Vector


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds the different types of ores; inherits from OccupiableStation.
    """

    def __init__(self, position: Vector, seed: float, special_weight: float, ancient_tech_weight: float):
        super().__init__(held_item=Copium())
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION
        self.rand = random.Random((19 * position.y + 23 * position.y) * seed)
        self.special_weight = special_weight
        self.ancient_tech_weight = ancient_tech_weight

    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager = None) -> None:
        if InventoryManager is None or not isinstance(inventory_manager, InventoryManager):
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, avatar.company)

        if isinstance(self.held_item, Copium):
            generated_num: float = self.rand.random()

            if generated_num <= self.special_weight / 2:
                self.held_item = Lambdium()
            elif generated_num <= self.special_weight:
                self.held_item = Turite()
            else:
                generated_num = self.rand.random()

                if generated_num <= self.ancient_tech_weight:
                    self.held_item = AncientTech()
                else:
                    self.held_item = None
        elif isinstance(self.held_item, Turite) or isinstance(self.held_item, Lambdium):
            generated_num = self.rand.random()

            if generated_num <= self.ancient_tech_weight:
                self.held_item = AncientTech()
            else:
                self.held_item = None

        else:
            self.held_item = None
