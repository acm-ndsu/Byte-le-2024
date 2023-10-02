import os

import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector


class EmpsBS(ByteSprite):
    def __init__(self, screen: pyg.Surface):
        super().__init__(screen, os.path.join(os.getcwd(), 'visualizer/dummy_sprites/EMPS.png'), 1, None, 31)

    def update(self, data: dict, layer: int, pos: Vector) -> None:
        super().update(data, layer, pos)
        self.active_sheet = self.spritesheets[0]

        self.set_image_and_render()