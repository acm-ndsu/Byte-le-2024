import os
import random

import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector


class ExampleBS(ByteSprite):
    def __init__(self, screen: pyg.Surface):
        super().__init__(screen, os.path.join(os.getcwd(), 'visualizer/spritesheets/ExampleSpritesheet.png'), 4,
                         pyg.Color("#FBBBAD"), 4)

    def update(self, data: dict, layer: int, pos: Vector) -> None:
        super().update(data, layer, pos)

        # Logic for selecting active animation
        if data['inventory'][data['held_index']] is not None:
            self.active_sheet = self.spritesheets[1]
        elif random.randint(1, 6) == 6:
            self.active_sheet = self.spritesheets[2]
        elif random.randint(1, 4) == 4:
            self.active_sheet = self.spritesheets[3]
        else:
            self.active_sheet = self.spritesheets[0]

        self.set_image_and_render()
