import os
import random

import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class TileBS(ByteSpriteFactory):
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        if random.randint(1, 6) == 6:
            return spritesheets[1]

        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/ExampleTileSS.png'), 2,
                          7, TileBS.update)
