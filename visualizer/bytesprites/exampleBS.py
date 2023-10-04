import os
import random

import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class AvatarBytespriteFactoryExample(ByteSpriteFactory):
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        # Logic for selecting active animation
        if data['inventory'][data['held_index']] is not None:
            return spritesheets[1]
        elif random.randint(1, 6) == 6:
            return spritesheets[2]
        elif random.randint(1, 4) == 4:
            return spritesheets[3]
        else:
            return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/ExampleSpritesheet.png'), 4,
                          4, AvatarBytespriteFactoryExample.update, pyg.Color("#FBBBAD"))
