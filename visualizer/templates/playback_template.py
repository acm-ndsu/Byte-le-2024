import os
from dataclasses import dataclass
from functools import reduce
from enum import Flag, auto

import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button, ButtonColors
from visualizer.utils.text import Text

"""
This file is for creating a default template for the playback implementation for the Visualizer. This will be displayed
while the game is running, with buttons including pause, speed up, slow down, restart, and save to mp4.
"""


class PlaybackButtons(Flag):
    PAUSE_BUTTON = auto()
    SAVE_BUTTON = auto()
    NEXT_BUTTON = auto()
    PREV_BUTTON = auto()
    START_BUTTON = auto()
    END_BUTTON = auto()
    NORMAL_SPEED_BUTTON = auto()
    FAST_SPEED_BUTTON = auto()
    FASTEST_SPEED_BUTTON = auto()


class PlaybackTemplate:
    """
    Playback Template provides a menu of buttons during runtime of the visualizer to control the playback
    of the visualizer, including pausing, start, end, frame scrubbing, speeding up, and slowing down, as well as
    saving it to .mp4

    Buttons from this template are centered at the bottom of the screen, placed in three rows of three
    """

    def __init__(self, screen: pygame.Surface):
        font = os.path.join(os.getcwd(), r'visualizer\templates\zrnic rg.otf')
        colors = ButtonColors(bg_color='#A26D3F',
                              bg_color_hover='#CE9248',
                              bg_color_clicked='#94493A',
                              fg_color='#DAB163',
                              fg_color_hover='#36C5F4',
                              fg_color_clicked='#FA6E79')
        self.screen: pygame.Surface = screen
        self.pause_button: Button = Button(self.screen, 'Pause', lambda: PlaybackButtons.PAUSE_BUTTON, font_size=18,
                                           colors=colors, font_name=font)
        self.next_button: Button = Button(self.screen, 'Next', lambda: PlaybackButtons.NEXT_BUTTON, font_size=18,
                                          colors=colors, font_name=font)
        self.prev_button: Button = Button(self.screen, 'Prev', lambda: PlaybackButtons.PREV_BUTTON, font_size=18,
                                          colors=colors, font_name=font)
        self.start_button: Button = Button(self.screen, 'Start', lambda: PlaybackButtons.START_BUTTON, font_size=18,
                                           colors=colors, font_name=font)
        self.end_button: Button = Button(self.screen, 'End', lambda: PlaybackButtons.END_BUTTON, font_size=18,
                                         colors=colors, font_name=font)
        self.save_button: Button = Button(self.screen, 'Save', lambda: PlaybackButtons.SAVE_BUTTON, font_size=18,
                                          colors=colors, font_name=font)
        self.normal_speed_button: Button = Button(self.screen, '1x', lambda: PlaybackButtons.NORMAL_SPEED_BUTTON,
                                                  font_size=18, colors=colors, font_name=font)
        self.fast_speed_button: Button = Button(self.screen, '2x', lambda: PlaybackButtons.FAST_SPEED_BUTTON,
                                                font_size=18, colors=colors, font_name=font)
        self.fastest_speed_button: Button = Button(self.screen, '4x', lambda: PlaybackButtons.FASTEST_SPEED_BUTTON,
                                                   font_size=18, colors=colors, font_name=font)

        self.prev_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(-80, 225)).as_tuple()
        self.pause_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(0, 225)).as_tuple()
        self.next_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(80, 225)).as_tuple()
        self.start_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                           Vector(-80, 275)).as_tuple()
        self.save_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                          Vector(0, 275)).as_tuple()
        self.end_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                         Vector(80, 275)).as_tuple()
        self.normal_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                  Vector(-80, 325)).as_tuple()
        self.fast_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                Vector(0, 325)).as_tuple()
        self.fastest_speed_button.rect.center = Vector.add_vectors(Vector(*self.screen.get_rect().center),
                                                                   Vector(80, 325)).as_tuple()

    def playback_render(self) -> None:
        self.prev_button.render()
        self.pause_button.render()
        self.next_button.render()
        self.start_button.render()
        self.save_button.render()
        self.end_button.render()
        self.normal_speed_button.render()
        self.fast_speed_button.render()
        self.fastest_speed_button.render()

    def playback_events(self, event: pygame.event) -> PlaybackButtons:
        return reduce(lambda a, b: a | b,
                      (self.pause_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.save_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.next_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.prev_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.start_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.end_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.normal_speed_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.fast_speed_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.fastest_speed_button.mouse_clicked(event, default=PlaybackButtons(0))))
