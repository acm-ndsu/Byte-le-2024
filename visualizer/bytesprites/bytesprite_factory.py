import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg

from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite import ByteSprite


class ByteSpriteFactory:
    """
    This is a class that every ByteSpriteFactory subclass must inherit. The factory structure allows for these classes
    to create the ByteSprite objects that will be used for visualization. With the given structure, it forces those
    classes to have the following methods: update() and create_bytesprite(). These methods can be implemented in many
    different ways depending on how the sprites should behave during the game. Examples are provided in the example
    files.
    """
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
