import os
import random

import pygame
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class OreStationBS(ByteSpriteFactory):

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        # 0 -> Copium (13); 1 -> Lambdium (11); 2 -> Turite (12); 3 -> Ancient Tech (15)
        ore_type: int = data.get('held_item', {'object_type': 1})['object_type']
        offset: int = 0 if ore_type == 13 else \
            1 if ore_type == 11 else \
            2 if ore_type == 12 else \
            3 if ore_type == 15 else 4

        if offset == 4:
            raise ValueError('Unspecified ore ObjectType in OreStationBS.update')

        if random.randint(1, 6) == 6:
            return spritesheets[offset * 2 + 1]

        return spritesheets[offset * 2]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/OreSS.png'), 8, 30,
                          OreStationBS.update, colorkey=pygame.Color(255, 0, 255))
