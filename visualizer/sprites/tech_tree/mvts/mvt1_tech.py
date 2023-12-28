import pygame
import os

from game.utils.vector import Vector


class Mvt1Tech(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: list[pygame.Surface] = [
            pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/tech_tree/mvts/mvt1-deactivated-tech-tree.png')),
            pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/tech_tree/mvts/mvt1-activated-tech-tree.png'))
        ]
        self.image: pygame.Surface = self.images[0]
        self.activated: bool = False
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

        @property
        def activated(self) -> bool:
            return self.__activated

        @activated.setter
        def activated(self, activated) -> None:
            self.__activated = activated
            self.image = self.images[1 if self.__activated else 0]