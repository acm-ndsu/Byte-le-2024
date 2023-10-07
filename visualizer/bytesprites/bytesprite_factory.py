import pygame as pyg

from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite import ByteSprite


class ByteSpriteFactory:
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        """
        This is a method that **must** be implemented in every ByteSpriteFactory class. Look at the example files
        to see how this *could* be implemented. Implementation may vary.
        :param data:
        :param layer:
        :param pos:
        :param spritesheets:
        :return: list[pyg.Surface]
        """
        ...

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        """
        This is a method that **must** be implemented in every ByteSpriteFactory class. Look at the example files
        to see how this can be implemented.
        :param screen:
        :return:
        """
        ...
