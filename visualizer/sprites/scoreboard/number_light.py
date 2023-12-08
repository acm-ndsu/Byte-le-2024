import pygame
import os

from game.utils.vector import Vector


class NumberLight(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        # TODO: Add Correct sprite locations
        self.images: list[pygame.Surface] = [
            pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/inventory/landmine-deactivated-inventory.png')),
            pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/inventory/landmine-activated-inventory.png'))
        ]
        self.image: pygame.Surface = self.images[0]
        self.character: int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

        @property
        def character(self) -> int:
            return self.__character

        @character.setter
        def character(self, character: int) -> None:
            self.__character = character
            self.image = self.images[character]
