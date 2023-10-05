from __future__ import annotations
from typing import Callable

import pygame as pyg

from visualizer.config import Config
from visualizer.utils.spritesheet import SpriteSheet
from game.utils.vector import Vector


class ByteSprite(pyg.sprite.Sprite):
    active_sheet: list[pyg.Surface]  # The current spritesheet being used.
    spritesheets: list[list[pyg.Surface]]
    object_type: int
    layer: int
    rect: pyg.Rect
    screen: pyg.Surface
    image: pyg.Surface
    __frame_index: int  # Selects the sprite from the spritesheet to be used. Used for animation
    __config: Config = Config()
    __update_function: Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]]

    # make sure that all inherited classes constructors only take screen as a parameter
    def __init__(self, screen: pyg.Surface, filename: str, num_of_states: int, object_type: int,
                 update_function: Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]],
                 colorkey: pyg.Color | None = None, layer: int = 0, top_left: Vector = Vector(0, 0)):
        # Add implementation here for selecting the sprite sheet to use
        super().__init__()
        self.spritesheet_parser: SpriteSheet = SpriteSheet(filename)
        self.spritesheets: list[list[pyg.Surface]] = [self.spritesheet_parser.load_strip(
            pyg.Rect(0, self.__config.TILE_SIZE * row, self.__config.TILE_SIZE, self.__config.TILE_SIZE),
            self.__config.NUMBER_OF_FRAMES_PER_TURN, colorkey)
            for row in range(num_of_states)]

        self.rect: pyg.Rect = pyg.Rect(top_left.as_tuple(), (self.__config.TILE_SIZE * self.__config.SCALE,) * 2)

        self.spritesheets = [
            [pyg.transform.scale(frame, self.rect.size) for frame in
             sheet] for sheet in self.spritesheets]

        self.update_function = update_function

        self.active_sheet: list[pyg.Surface] = self.spritesheets[0]
        self.object_type: int = object_type
        self.screen: pyg.Surface = screen
        self.layer: int = layer

    @property
    def active_sheet(self) -> list[pyg.Surface]:
        return self.__active_sheet

    @property
    def spritesheets(self) -> list[list[pyg.Surface]]:
        return self.__spritesheets

    @property
    def object_type(self) -> int:
        return self.__object_type

    @property
    def layer(self) -> int:
        return self.__layer

    @property
    def rect(self) -> pyg.Rect:
        return self.__rect

    @property
    def screen(self) -> pyg.Surface:
        return self.__screen

    @property
    def update_function(self) -> Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]]:
        return self.__update_function

    @active_sheet.setter
    def active_sheet(self, sheet: list[pyg.Surface]) -> None:
        if sheet is None or not isinstance(sheet, list) and \
                any(map(lambda sprite: not isinstance(sprite, pyg.Surface), sheet)):
            raise ValueError(f'{self.__class__.__name__}.active_sheet must be a list of pyg.Surface objects.')
        self.__active_sheet = sheet

    @spritesheets.setter
    def spritesheets(self, spritesheets: list[list[pyg.Surface]]) -> None:
        if spritesheets is None or (
                not isinstance(spritesheets, list) or any(map(lambda sheet: not isinstance(sheet, list), spritesheets))
                or any([any(map(lambda sprite: not isinstance(sprite, pyg.Surface), sheet))
                        for sheet in spritesheets])):
            raise ValueError(f'{self.__class__.__name__}.spritesheets must be a list of lists of pyg.Surface objects.')

        self.__spritesheets = spritesheets

    @object_type.setter
    def object_type(self, object_type: int) -> None:
        if object_type is None or not isinstance(object_type, int):
            raise ValueError(f'{self.__class__.__name__}.object_type must be an int.')

        if object_type < 0:
            raise ValueError(f'{self.__class__.__name__}.object_type can\'t be negative.')
        self.__object_type = object_type

    @layer.setter
    def layer(self, layer: int) -> None:
        if layer is None or not isinstance(layer, int):
            raise ValueError(f'{self.__class__.__name__}.layer must be an int.')

        if layer < 0:
            raise ValueError(f'{self.__class__.__name__}.layer can\'t be negative.')
        self.__layer = layer

    @rect.setter
    def rect(self, rect: pyg.Rect) -> None:
        if rect is None or not isinstance(rect, pyg.Rect):
            raise ValueError(f'{self.__class__.__name__}.rect must be a pyg.Rect object.')
        self.__rect = rect

    @screen.setter
    def screen(self, screen: pyg.Surface) -> None:
        if screen is None or not isinstance(screen, pyg.Surface):
            raise ValueError(f'{self.__class__.__name__}.screen must be a pyg.Screen object.')
        self.__screen = screen

    @update_function.setter
    def update_function(self, update_function: Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]]) -> None:
        if update_function is None or not isinstance(update_function, Callable):
            raise ValueError(f'{self.__class__.__name__}.update_function must be a Callable object.')
        self.__update_function = update_function

    # Inherit this method to implement sprite logic
    def update(self, data: dict, layer: int, pos: Vector) -> None:

        self.__frame_index = 0  # Starts the new spritesheet at the beginning
        self.rect.topleft = (
            pos.x * self.__config.TILE_SIZE * self.__config.SCALE + self.__config.GAME_BOARD_MARGIN_LEFT,
            pos.y * self.__config.TILE_SIZE * self.__config.SCALE + self.__config.GAME_BOARD_MARGIN_TOP)

        self.update_function(data, layer, pos, self.spritesheets)
        self.set_image_and_render()

    # Call this method at the end of the implemented logic and for each frame
    def set_image_and_render(self):
        self.image = self.active_sheet[self.__frame_index]
        self.__frame_index = (self.__frame_index + 1) % self.__config.NUMBER_OF_FRAMES_PER_TURN
        self.screen.blit(self.image, self.rect)


