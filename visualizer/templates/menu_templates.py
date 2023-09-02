from typing import Any

import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button
from visualizer.utils.text import Text

"""
This is file is for creating different templates for the start menu of the visualizer. Each different menu screen 
will be a different class. The Basic class is the default template for the screen. Create extra classes for 
different start menu screens. The Basic class can be used as a template on how to do so.
"""


class MenuTemplate:
    """
    Menu Template is used as an interface. It provides a screen object from pygame.Surface and a start and
    results button. These are common attributes to all menus, so they are provided to facilitate creating them.

    This class also provides methods that are expanded upon in the Basic class. Refer to that class' documentation
    for further detail. These provided methods can be used via inheritance and expanded upon as needed.

    -----
    Note: The provided buttons are already centered to be in the center of the screen.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.start_button: Button = Button(screen, 'Start Game', lambda: False, font_size=24, padding=10)
        self.results_button: Button = Button(screen, 'Exit', lambda: False, font_size=24, padding=10)
        self.start_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(0, 100)).as_tuple()

        self.results_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                             Vector(0, 100)).as_tuple()

    def start_events(self, event: pygame.event) -> Any:
        return self.start_button.mouse_clicked(event) if self.start_button.mouse_clicked(
            event) is not None else True

    def start_render(self) -> None:
        self.start_button.render()

    def load_results_screen(self, results: dict): ...

    def results_events(self, event: pygame.event) -> Any:
        return self.results_button.mouse_clicked(event) if self.results_button.mouse_clicked(
            event) is not None else True

    def results_render(self) -> None:
        self.results_button.render()


class Basic(MenuTemplate):
    """
    The Basic class is a default template that can be used for the menu screens. It inherits from MenuTemplate and
    expands on the inherited methods. If different templates are desired, create more classes in this file. This
    Basic class can be used as a template for any future classes.
    """

    def __init__(self, screen: pygame.Surface, title: str):
        super().__init__(screen)
        self.title: Text = Text(screen, title, 48)
        self.title.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                    Vector(0, -100)).as_tuple()

        self.winning_team_name: Text = Text(screen, '', 0)

    def start_render(self) -> None:
        super().start_render()
        self.title.render()

    def load_results_screen(self, results: dict) -> None:
        winning_teams = self.__get_winning_teams(results['players'])
        self.winning_team_name = Text(self.screen, winning_teams, 36)
        self.winning_team_name.rect.center = self.screen.get_rect().center

    def results_render(self) -> None:
        super().results_render()
        self.title.render()
        self.winning_team_name.render()

    def __get_winning_teams(self, players: list) -> str:
        m = max(map(lambda player: player['avatar']['score'], players))  # Gets the max score from all results

        # Compares each player in the given list to the max score
        winners: list = [player['team_name'] for player in players if player['avatar']['score'] == m]

        # Prints the winner(s) from the final results
        return f'{"Winners" if len(winners) > 1 else "Winner"}: {", ".join(winners)}'
