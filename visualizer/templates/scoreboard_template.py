import pygame

from game.utils.vector import Vector
from visualizer.sprites.scoreboard.scoreboard_backdrop import ScoreboardBackdrop
from visualizer.templates.info_template import InfoTemplate


class ScoreboardTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str) -> None:
        super().__init__(screen, topleft, size, font, color)

        self.scoreboard_backdrop: ScoreboardBackdrop = ScoreboardBackdrop(top_left=Vector())
        self.scoreboard_backdrop.add(self.render_list)

        ...

    def recalc_animation(self, turn_log: dict) -> None:
        ...
