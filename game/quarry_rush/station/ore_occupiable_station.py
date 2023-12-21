import random
from game.common.enums import ObjectType, Company
from game.common.game_object import GameObject
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.entity.ores import Lambdium, Turite, Copium
from game.utils.vector import Vector
from game.common.map.tile import Tile


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds the different types of ores; inherits from OccupiableStation.
    """

    def __init__(self, position: Vector = Vector(0, 0), seed: float = 0, special_weight: float = .2,
                 ancient_tech_weight: float = .1):
        super().__init__(held_item=Copium())
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION
        self.rand = random.Random((19 * position.y + 23 * position.y) * seed)
        self.special_weight = special_weight
        self.ancient_tech_weight = ancient_tech_weight
        self.held_item = Copium()

    def give_item(self, company: Company, inventory_manager: InventoryManager = None) -> None:
        if InventoryManager is None or not isinstance(inventory_manager, InventoryManager):
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        inventory_manager.give(self.held_item, company)

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

    def remove_from_game_board(self, tile: Tile):
        """
        By giving a tile object, it will remove this OreOccupiableStation object from it.
        """
        if self.held_item is None:
            tile.remove_from_occupied_by(ObjectType.ORE_OCCUPIABLE_STATION)
    