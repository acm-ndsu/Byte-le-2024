import pygame as pyg

from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite import ByteSprite


class ByteSpriteFactory:
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        ...

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        ...
