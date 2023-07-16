from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.quarry_rush.inventory_manager import InventoryManager
from typing import Self


class Dynamite(GameObject):
    def __init__(self, inventory_manager: InventoryManager, position: Vector | None = None,
                 blast_radius: int = 1, detonate_turn: int = 1):
        super().__init__()
        self.inventory_manager: InventoryManager = inventory_manager
        self.position: Vector | None = position
        self.blast_radius: int = blast_radius
        self.detonate_turn: int = detonate_turn

    # inventory manager getter
    @property
    def inventory_manager(self) -> InventoryManager:
        return self.__inventory_manager

    # inventory manager setter
    @inventory_manager.setter
    def inventory_manager(self, inventory_manager: InventoryManager) -> None:
        if inventory_manager is None or not isinstance(inventory_manager, InventoryManager):
            raise ValueError(
                f'{self.__class__.__name__}.inventory_manager must be of type InventoryManager.')
        if hasattr(self, '__inventory_manager') and self.__inventory_manager is not None:
            raise ValueError(
                f'{self.__class__.__name__}.inventory_manager has already been set.')
        self.__inventory_manager = inventory_manager

    # position getter
    @property
    def position(self) -> Vector | None:
        return self.__position

    # position setter
    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position: Vector | None = position

    # blast radius getter
    @property
    def blast_radius(self) -> int:
        return self.__blast_radius

    # blast radius setter
    @blast_radius.setter
    def blast_radius(self, blast_radius: int) -> None:
        if blast_radius is None or not isinstance(blast_radius, int):
            raise ValueError(f'{self.__class__.__name__}.blast_radius must be an int.')
        self.__blast_radius: int = blast_radius

    # detonate_turn getter
    @property
    def detonate_turn(self) -> int:
        return self.__detonate_turn

    # detonate_turn setter
    @detonate_turn.setter
    def detonate_turn(self, detonate_turn: int) -> None:
        if detonate_turn is None or not isinstance(detonate_turn, int):
            raise ValueError(f'{self.__class__.__name__}.blast_radius must be an int')
        self.__detonate_turn = detonate_turn

    # detonate method
    def detonate(self, current_turn: int):
        if current_turn is self.__detonate_turn:
            self.explode()

    # explode dynamite
    def explode(self):
        above_tile: list[Vector] = [Vector(self.position.x, self.position.y - adjacent) for adjacent in
                                    range(1, self.blast_radius + 1)]  # Getting tiles above
        below_tile: list[Vector] = [Vector(self.position.x, self.position.y + adjacent) for adjacent in
                                    range(1, self.blast_radius + 1)]  # Getting tiles below
        left_tile: list[Vector] = [Vector(self.position.x - adjacent, self.position.y) for adjacent in
                                   range(1, self.blast_radius + 1)]  # Getting tiles left
        right_tile: list[Vector] = [Vector(self.position.x + adjacent, self.position.y) for adjacent in
                                    range(1, self.blast_radius + 1)]  # Getting tiles right
        # add all the tile lists together
        adjacent_tiles: list[Vector] = above_tile + below_tile + left_tile + right_tile

    # collection method - not yet, foods still cooking
    # wip

    # to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['inventory_manager'] = self.inventory_manager.to_json()
        data['position'] = self.position.to_json() if self.position is not None else None
        data['blast_radius'] = self.blast_radius
        data['detonate_turn'] = self.detonate_turn
        return data

    # from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.inventory_manager: InventoryManager = InventoryManager().from_json(data['inventory_manager'])
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.blast_radius: int = data['blast_radius']
        self.detonate_turn: int = data['detonate_turn']
        return self

