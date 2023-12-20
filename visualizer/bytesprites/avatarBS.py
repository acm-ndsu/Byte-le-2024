import os
import random

import pygame
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class AvatarBS(ByteSpriteFactory):

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        offset: int = 5 if data.get('company', 0) == 2 else 0

        return spritesheets[offset]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/avatar.png'), 10, 4,
                          AvatarBS.update, colorkey=pygame.Color(255, 0, 255))
