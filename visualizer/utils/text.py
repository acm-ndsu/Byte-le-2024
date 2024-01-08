import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game.utils.vector import Vector
from typing import Optional, TypeAlias

# Typing alias for color
Color: TypeAlias = str | int | tuple[int, int, int, Optional[int]] | list[
    int, int, int, Optional[int]] | pygame.Color


class Text:
    """
    Class that creates text to be displayed in the visualizer

    Defaults used unless otherwise stated:
    font: Bauhaus93
    color: #daa520          (yellowish)
    position: Vector(0, 0)  (representing pixels on screen, top left pixel)

    Parameters:
    screen          :  Screen being used for display
    font_size       :  Font size used for text
    font_name       :  Name of font used for text
    color           :  Color used for text
    position        :  Position of text to be displayed
    text            :  Text to be displayed

    In future projects, defaults for text style should be changed according to style of game for ease of code
    """

    def __init__(self, screen: pygame.Surface, text: str, font_size: int, font_name: str = 'bauhaus93',
                 color: Color = pygame.Color('#daa520'), position: Vector = Vector(0, 0)):
        self.__is_init = True
        self.screen: pygame.Surface = screen
        self.font_size: int = font_size
        self.font_name: str = font_name
        # Get selected font from list of fonts
        try:
            self.__font: pygame.font.Font = pygame.font.Font(self.font_name, self.font_size)
        except FileNotFoundError:
            self.__font: pygame.font.Font = pygame.font.SysFont(self.font_name, self.font_size)
        self.color: Color = color
        self.position: Vector = position
        self.text: str = text
        # SysFont, adjust size
        # Render text with color
        self.__text_surface: pygame.Surface = self.__font.render(self.text, True, self.color)
        # get rectangle used
        self.__rect: pygame.Rect = self.__text_surface.get_rect()
        # Set top left position of rect to position
        self.__rect.topleft = self.position.as_tuple()
        self.__is_init = False

    # Render text and rectangle to screen
    def render(self) -> None:
        self.position = Vector(*self.__rect.topleft)
        self.screen.blit(self.__text_surface, self.__rect)

    # Getter methods
    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @property
    def text(self) -> str:
        return self.__text

    @property
    def font_name(self) -> str:
        return self.__font_name

    @property
    def font_size(self) -> int:
        return self.__font_size

    @property
    def color(self) -> pygame.Color:
        return self.__color

    @property
    def position(self) -> Vector:
        return self.__position

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    # Setter methods
    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        if screen is None or not isinstance(screen, pygame.Surface):
            raise ValueError(f'{self.__class__.__name__}.screen must be of type pygame.Surface.')
        self.__screen: pygame.Surface = screen

    @text.setter
    def text(self, text: str) -> None:
        if text is None or not isinstance(text, str):
            raise ValueError(f'{self.__class__.__name__}.text must be a str.')
        self.__text: str = text
        # Reevaluate text
        self.__text_surface: pygame.Surface = self.__font.render(self.text, True, self.color)
        self.__rect: pygame.Rect = self.__text_surface.get_rect()
        self.__rect.topleft = self.position.as_tuple()

    @font_name.setter
    def font_name(self, font_name: str) -> None:
        if font_name is None or not isinstance(font_name, str):
            raise ValueError(f'{self.__class__.__name__}.font_name must be a str.')
        self.__font_name: str = font_name
        if self.__is_init: return
        # Reevaluate text with new font
        self.__font: pygame.font.Font = pygame.font.SysFont(self.font_name, self.font_size)
        self.__text_surface: pygame.Surface = self.__font.render(self.text, True, self.color)
        self.__rect: pygame.Rect = self.__text_surface.get_rect()
        self.__rect.topleft = self.position.as_tuple()

    @font_size.setter
    def font_size(self, font_size: int) -> None:
        if font_size is None or not isinstance(font_size, int):
            raise ValueError(f'{self.__class__.__name__}.font_size must be an int.')
        self.__font_size: int = font_size
        if self.__is_init: return
        # Reevaluate text with new font size
        self.__font: pygame.font.Font = pygame.font.SysFont(self.font_name, self.font_size)
        self.__text_surface: pygame.Surface = self.__font.render(self.text, True, self.color)
        self.__rect: pygame.Rect = self.__text_surface.get_rect()
        self.__rect.topleft = self.position.as_tuple()

    @color.setter
    def color(self, color: Color) -> None:
        try:
            self.__color: pygame.Color = pygame.Color(color)
            if self.__is_init:
                return
            # Reevaluate text with new font color
            self.__text_surface: pygame.Surface = self.__font.render(self.text, True, self.color)
            self.__rect: pygame.Rect = self.__text_surface.get_rect()
            self.__rect.topleft = self.position.as_tuple()
        except (ValueError, TypeError):
            raise ValueError(
                f'{self.__class__.__name__}.color must be a one of the following types: str or int or tuple(int, int, '
                f'int, [int]) or list(int, int, int, [int]) or pygame.Color.')

    @position.setter
    def position(self, position: Vector) -> None:
        if position is None or not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector.')
        self.__position: Vector = position
        if self.__is_init:
            return
        # Reevaluate text position with new position
        self.__rect.topleft = self.position.as_tuple()
