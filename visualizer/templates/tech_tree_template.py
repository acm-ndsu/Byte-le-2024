import pygame

from game.utils.vector import Vector
from visualizer.templates.info_template import InfoTemplate


class TechTreeTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str, player: int) -> None:
        super().__init__(screen, topleft, size, font, color)
        self.player = player

    def recalc_animation(self, turn_log: dict) -> None:
        ...