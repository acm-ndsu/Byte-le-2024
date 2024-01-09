import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game.config import *
from typing import Callable, Any

from visualizer.bytesprites.avatarBS import AvatarBS
from visualizer.bytesprites.churchStationBS import ChurchStationBS
from visualizer.bytesprites.dynamiteBS import DynamiteBS
from visualizer.bytesprites.empsBS import EmpsBS
from game.utils.vector import Vector
from visualizer.bytesprites.landmineBS import LandmineBS
from visualizer.bytesprites.tileBS import TileBS
from visualizer.bytesprites.turingStationBS import TuringStationBS
from visualizer.bytesprites.oreStationBS import OreStationBS
from visualizer.bytesprites.wallBS import WallBS
from visualizer.config import Config
from visualizer.templates.inventory_template import InventoryTemplate
from visualizer.templates.scoreboard_template import ScoreboardTemplate
from visualizer.templates.tech_tree_template import TechTreeTemplate
from visualizer.utils.text import Text
from visualizer.utils.button import Button, ButtonColors
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
        self.config: Config = Config()
        self.bytesprites: list[ByteSprite] = []
        self.menu: MenuTemplate = Basic(screen, self.config.FONT,self.config.TEXT_COLOR, self.config.BUTTON_COLORS, 'Quarry Rush')
        self.playback: PlaybackTemplate = PlaybackTemplate(screen, self.config.FONT, self.config.BUTTON_COLORS)
        self.turn_number: int = 0
        self.turn_max: int = MAX_TICKS
        self.scoreboard = ScoreboardTemplate(screen, Vector(), Vector(y=100, x=1366), self.config.FONT, self.config.TEXT_COLOR)
        self.p1_tech_tree = TechTreeTemplate(screen, Vector(y=548), Vector(y=220, x=459), self.config.FONT, self.config.TEXT_COLOR, 1)
        self.p1_inventory = InventoryTemplate(screen, Vector(y=100), Vector(y=448, x=459), self.config.FONT, self.config.TEXT_COLOR, 1)
        self.p2_tech_tree = TechTreeTemplate(screen, Vector(y=548, x=907), Vector(y=220, x=459), self.config.FONT, self.config.TEXT_COLOR, 2)
        self.p2_inventory = InventoryTemplate(screen, Vector(y=100, x=907), Vector(y=448, x=459), self.config.FONT, self.config.TEXT_COLOR, 2)



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

    # re-renders the animation
    def recalc_animation(self, turn_log: dict) -> None:
        self.scoreboard.recalc_animation(turn_log)
        self.p1_inventory.recalc_animation(turn_log)
        self.p2_inventory.recalc_animation(turn_log)
        self.p1_tech_tree.recalc_animation(turn_log)
        self.p2_tech_tree.recalc_animation(turn_log)
        self.turn_number = turn_log['tick']

    def populate_bytesprite_factories(self) -> dict[int: Callable[[pygame.Surface], ByteSprite]]:
        # Instantiate all bytesprites for each object ands add them here
        return {
            4: AvatarBS.create_bytesprite,
            7: TileBS.create_bytesprite,
            8: WallBS.create_bytesprite,
            22: ChurchStationBS.create_bytesprite,
            23: TuringStationBS.create_bytesprite,
            29: DynamiteBS.create_bytesprite,
            30: OreStationBS.create_bytesprite,
            32: LandmineBS.create_bytesprite,
            33: EmpsBS.create_bytesprite,
        }

    def render(self) -> None:
        # self.button.render()
        # any logic for rendering text, buttons, and other visuals
        text = Text(self.screen, f'{self.turn_number:3d} / {self.turn_max:3d}', 48, color=self.config.TEXT_COLOR,
                    font_name=self.config.FONT)
        text.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().midtop), Vector(0, 50)).as_tuple()
        text.render()

        self.p1_inventory.render()
        self.p2_inventory.render()
        self.p1_tech_tree.render()
        self.p2_tech_tree.render()
        self.scoreboard.render()
        self.playback.playback_render()

    # is used in post render - post render is used to clear the playback buttons
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

