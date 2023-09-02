import os

import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector


class ExampleTileBS(ByteSprite):
    def __init__(self, screen: pyg.Surface):
        super().__init__(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/ExampleTileSS.png'), 2, None, 7)

    def update(self, data: dict, layer: int, pos: Vector) -> None:
        super().update(data, layer, pos)
        if data['occupied_by'] is not None:
            self.active_sheet = self.spritesheets[1]
        else:
            self.active_sheet = self.spritesheets[0]

        self.set_image_and_render()
