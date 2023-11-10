from game.utils.vector import Vector
from game.common.stations.occupiable_station import OccupiableStation
from game.common.enums import *
from typing import Self


class Dynamite(OccupiableStation):
    """
    Dynamite is a class that represents the dynamite an Avatar can place on the ground. It inherits from Occupiable
    Station to permit Avatar instances to walk on them.
    """
    def __init__(self, position: Vector | None = None, blast_radius: int = 0):
        super().__init__()
        self.position: Vector | None = position
        self.blast_radius: int = blast_radius
        self.fuse: int = 1
        self.object_type = ObjectType.DYNAMITE

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

    def decrement_fuse(self) -> None:
        self.fuse = max(self.fuse - 1, 0)

    def can_explode(self) -> bool:
        return self.fuse == 0

    # # detonate method
    # def detonate(self, inventory_manager: InventoryManager):
    #     self.fuse -= 1
    #     if self.fuse <= 0:
    #         self.explode()
    #         return True
    #     return False

    # explode dynamite
    # def explode(self):
        # above_tile: list[Vector] = [Vector(self.position.x, self.position.y - adjacent) for adjacent in
        #                             range(1, self.blast_radius + 1)]  # Getting tiles above
        # below_tile: list[Vector] = [Vector(self.position.x, self.position.y + adjacent) for adjacent in
        #                             range(1, self.blast_radius + 1)]  # Getting tiles below
        # left_tile: list[Vector] = [Vector(self.position.x - adjacent, self.position.y) for adjacent in
        #                            range(1, self.blast_radius + 1)]  # Getting tiles left
        # right_tile: list[Vector] = [Vector(self.position.x + adjacent, self.position.y) for adjacent in
        #                             range(1, self.blast_radius + 1)]  # Getting tiles right
        # # add all the tile lists together
        # adjacent_tiles: list[Vector] = above_tile + below_tile + left_tile + right_tile

    # def collect_ores(self):
    # collection method - not yet, foods still cooking
    # wip

    # to json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['position'] = self.position.to_json() if self.position is not None else None
        data['blast_radius'] = self.blast_radius
        return data

    # from json
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.blast_radius: int = data['blast_radius']
        return self
