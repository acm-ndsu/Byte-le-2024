import random

import pygame
from game.config import *
from typing import Callable, Any
from visualizer.bytesprites.exampleTileBS import ExampleTileBS
from visualizer.bytesprites.exampleWallBS import ExampleWallBS
from visualizer.bytesprites.exampleBS import ExampleBS
from visualizer.bytesprites.ancientTechBS import AncientTechBS
from visualizer.bytesprites.copiumBS import CopiumBS
from visualizer.bytesprites.dynamiteBS import DynamiteBS
from visualizer.bytesprites.empsBS import EmpsBS
from visualizer.bytesprites.lambdiumBS import LambdiumBS
from visualizer.bytesprites.landmineBS import LandmineBS
from visualizer.bytesprites.stationBS import StationBS
from visualizer.bytesprites.turiteBS import TuriteBS
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.utils.button import Button, ButtonColors
from visualizer.utils.sidebars import Sidebars
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.templates.menu_templates import Basic, MenuTemplate
from visualizer.templates.playback_template import PlaybackTemplate, PlaybackButtons


class Adapter:
    """
    The Adapter class can be considered the "Master Controller" of the Visualizer; it works in tandem with main.py.
    Main.py will call many of the methods that are provided in here to keep the Visualizer moving smoothly.
    """

    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.bytesprites: list[ByteSprite] = []
        self.populate_bytesprite: pygame.sprite.Group = pygame.sprite.Group()
        self.menu: MenuTemplate = Basic(screen, 'Basic Title')
        self.playback: PlaybackTemplate = PlaybackTemplate(screen)
        self.turn_number: int = 0
        self.turn_max: int = MAX_TICKS

    # Define any methods button may run

    def start_menu_event(self, event: pygame.event) -> Any:
        """
        This method is used to manage any events that will occur on the starting screen. For example, a start button
        is implemented currently. Pressing it or pressing enter will start the visualizer to show the game's results.
        This method will manage any specified events and return them (hence why the return type is Any). Refer to
        menu_templates.py's start_events method for more info.
        :param event:
        :return: Any specified event desired in the start_events method
        """
        return self.menu.start_events(event)

    def start_menu_render(self) -> None:
        """
        Renders and shows everything in the start menu.
        :return: None
        """
        self.menu.start_render()

    def on_event(self, event) -> PlaybackButtons:
        """
        By giving this method an event, this method can execute whatever is specified. An example is provided below
        and commented out. Use as necessary.
        :param event:
        :return: None
        """

        # The line below is an example of what this method could be used for.
        # self.button.mouse_clicked(event)
        return self.playback.playback_events(event)

    def prerender(self) -> None:
        """
        This will handle anything that needs to be completed before animations start.
        :return: None
        """
        ...

    def continue_animation(self) -> None:
        """
        This method is used after the main.py continue_animation() method.
        :return:
        """
        ...

    def recalc_animation(self, turn_log: dict) -> None:
        self.turn_number = turn_log['tick']

    def populate_bytesprites(self) -> pygame.sprite.Group:
        # Instantiate all bytesprites for each object ands add them here
        self.populate_bytesprite.add(ExampleTileBS(self.screen))
        self.populate_bytesprite.add(ExampleWallBS(self.screen))
        self.populate_bytesprite.add(ExampleBS(self.screen))
        self.populate_bytesprite.add(AncientTechBS(self.screen))
        self.populate_bytesprite.add(CopiumBS(self.screen))
        self.populate_bytesprite.add(DynamiteBS(self.screen))
        self.populate_bytesprite.add(EmpsBS(self.screen))
        self.populate_bytesprite.add(LambdiumBS(self.screen))
        self.populate_bytesprite.add(LandmineBS(self.screen))
        self.populate_bytesprite.add(StationBS(self.screen))
        self.populate_bytesprite.add(TuriteBS(self.screen))
        return self.populate_bytesprite.copy()

    def render(self) -> None:
        # self.button.render()
        # any logic for rendering text, buttons, and other visuals
        # to access sidebars do sidebars.[whichever sidebar you are doing]
        text = Text(self.screen, f'{self.turn_number} / {self.turn_max}', 48)
        text.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().midtop), Vector(0, 50)).as_tuple()
        text.render()
        self.playback.playback_render()

    def clean_up(self) -> None:
        ...

    def results_load(self, results: dict) -> None:
        self.menu.load_results_screen(results)

    def results_event(self, event: pygame.event) -> Any:
        return self.menu.results_events(event)

    def results_render(self) -> None:
        """
        This renders the results for the
        :return:
        """
        self.menu.results_render()

