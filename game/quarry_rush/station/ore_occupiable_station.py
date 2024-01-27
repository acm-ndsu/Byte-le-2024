import random
from game.common.enums import ObjectType, Company
from game.common.game_object import GameObject
from game.common.stations.occupiable_station import OccupiableStation
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from game.quarry_rush.entity.ancient_tech import AncientTech
from game.quarry_rush.entity.ores import Lambdium, Turite, Copium
from game.quarry_rush.entity.placeable.dynamite import Dynamite
from game.quarry_rush.entity.placeable.traps import Landmine, EMP
from game.utils.vector import Vector
from game.common.map.tile import Tile
from game.common.avatar import Avatar
from typing import Self


class OreOccupiableStation(OccupiableStation):
    """
    Station that holds the different types of ores; inherits from OccupiableStation.
    """

    def __init__(self, position: Vector = Vector(0, 0), seed: float = 0, special_weight: float = .2,
                 ancient_tech_weight: float = .1):
        super().__init__(held_item=Copium())
        self.object_type = ObjectType.ORE_OCCUPIABLE_STATION
        self.seed = seed
        self.position = position
        self.rand = random.Random((19 * position.x + 23 * position.y) * seed)
        self.special_weight = special_weight
        self.ancient_tech_weight = ancient_tech_weight
        self.held_item = Copium()

    def give_item(self, company: Company, inventory_manager: InventoryManager = None, drop_rate: int = 1) -> None:
        if InventoryManager is None or not isinstance(inventory_manager, InventoryManager):
            raise ValueError(f'{self.__class__.__name__}.take_action() needs an InventoryManager Object.')

        if drop_rate < 1:
            raise ValueError(f'{self.__class__.__name__}.give_item() needs a drop rate of at least 1')

        # gives the held item for the amount that is specified by the drop rate passed in
        for i in range(drop_rate):
            inventory_manager.give(self.held_item, company, drop_rate)

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
    
    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager):
        # The amount of ore received is equal to the avatar's drop rate. Make the change here when mined
        # Dynamite will not be affected by this, unless necessary for game balancing
        self.give_item(avatar.company, inventory_manager, avatar.drop_rate)

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['special_weight'] = self.special_weight
        data['ancient_tech_weight'] = self.ancient_tech_weight
        data['seed'] = self.seed
        data['position'] = self.position.to_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.special_weight = data['special_weight']
        self.ancient_tech_weight = data['ancient_tech_weight']
        self.seed = data['seed']
        self.position = Vector().from_json(data['position'])
        self.rand = random.Random((19 * self.position.x + 23 * self.position.y) * self.seed)
        if self.occupied_by is not None:
            return self
        occupied_by = data['occupied_by']
        if occupied_by is None:
            self.occupied_by = None
            return self
        # Add all possible game objects that can occupy a tile here (requires python 3.10)
        match ObjectType(occupied_by['object_type']):
            case ObjectType.DYNAMITE:
                self.occupied_by: Dynamite = Dynamite().from_json(occupied_by)
            case ObjectType.LANDMINE:
                self.occupied_by: Landmine = Landmine().from_json(occupied_by)
            case ObjectType.EMP:
                self.occupied_by: EMP = EMP().from_json(occupied_by)
            case _:
                raise Exception(f'Could not parse occupied_by: {occupied_by}')
        return self

    