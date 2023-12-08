import pygame
import os

from game.utils.vector import Vector


class ScoreboardBackdrop(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        # TODO: Add Correct sprite locations
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'visualizer/spritesheets/scoreboard_backdrop.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()
