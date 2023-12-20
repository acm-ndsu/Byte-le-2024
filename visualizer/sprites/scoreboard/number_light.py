import pygame
import os

from game.utils.vector import Vector


class NumberLight(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            0: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/zero-top-bar.png')),
            1: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/one-top-bar.png')),
            2: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/two-top-bar.png')),
            3: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/three-top-bar.png')),
            4: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/four-top-bar.png')),
            5: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/five-top-bar.png')),
            6: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/six-top-bar.png')),
            7: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/seven-top-bar.png')),
            8: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/eight-top-bar.png')),
            9: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/nine-top-bar.png')),
            '/': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/top_side_bar/slash-top-bar.png')),
        }

        self.image: pygame.Surface = self.images[0]
        self.character: str | int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def character(self) -> str | int:
        return self.__character

    @character.setter
    def character(self, character: str | int) -> None:
        self.__character = character
        self.image = self.images[character]
