from __future__ import annotations
from typing import Callable

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg

from visualizer.config import Config
from visualizer.utils.spritesheet import SpriteSheet
from game.utils.vector import Vector


class ByteSprite(pyg.sprite.Sprite):
    """
    `ByteSprite Class Notes:`

    PyGame Notes
    ------------
    Here are listed definitions of the PyGame objects that are used in this file:
        PyGame.Rect:
            "An object for storing rectangular coordinates." This is used to help position things on the screen.

        PyGame.Surface:
            "An object for representing images." This is used mostly for getting the screen and individual images in
            a spritesheet.


    Class Variables
    ---------------
        Active Sheet:
            The active_sheet is the list of images (sprites) that is currently being used. In other words, it's a strip
            of sprites that will be used.

        Spritesheets:
            This is a 2D array of sprites. For example, refer to the ``ExampleSpritesheet.png`` file. The entirety of the
            4x4 would be a spritesheet. One row of it would be used as an active sheet.

        Object Type:
            This is an int that represents the enum value of the Object the sprite represents. For example, the
            ``ExampleSpritesheet.png`` shows the Avatar. The Avatar object_type's enum value is found in the JSON logs and
            is the number 4. This would change if the order of the ObjectType enum changes, so be mindful of that and
            refer to the JSON logs for the exact values.

        Rect:
            The rect is an object used for rectangular objects. You can offset the top left corner of the Rect by
            passing parameters.

            Example:

            On the left, the Rect's offset is depicted as being at (0, 0),  meaning there is no offset. A Rect object
            has parameters that will determine the offset by passing in (x, y). The 'x' is the offset from the left
            side, and the 'y' is the offset from the top. Therefore, passing in an (x, y) of (3, 2) in a Rect object
            will move the object 3 units to the right, and 2 units down.

            In the visual below, the left side shows a Rect at (0, 0) (i.e., no offset). The image on the right depicts
            the Rect object further to the right, showing its offset from the left corner of the screen.

        Rect Example:
        ::
            -----------------------                 -----------------------
            |------               |                 |     ------          |
            ||    |               |                 |     |    |          |
            |______               |    -------->    |     ______          |
            |                     |                 |                     |
            |                     |                 |                     |
            |                     |                 |                     |
            -----------------------                 -----------------------

        Screen:
            The screen is also a PyGame.Screen object, so it simply represents an image of the screen itself.

        Image:
            The image is an individual sprite in a spritesheet.

        Frame Index:
            The frame index is an int that is used to determine which sprite to use from the active_sheet. For example,
            say the active_sheet is the first row in the ``ExampleSpritesheet.png``. If the frame_index is 1, the first
            image will be used where the head is centered. If the frame_index is 3, the sprite will now have the head of
            the Avatar in a different position than in frame_index 1.

        Config:
            This is an object reference to the ``config.py`` file. It's used to access the fixed values that are only
            accessed in the configurations of the file.

        Update Function:
            The update function is a method that is assigned during instantiation of the ByteSprite. That function is
            used to update what the active_sheet is depending on what is implemented in ByteSprite classes.

            Examine the ``exampleBS.py`` file. In that implementation of the update method, it selects the active_sheet
            based on a chain of if statements. Next, in the ``create_bytesprite`` method, the implemented ``update``
            method is passed into the returned ByteSprite object.

            Now, in the ByteSprite object's update method, it will set the active_sheet to be based on what is returned
            from the BytespriteFactory's method.

            To recap, first, a ByteSprite's update function depends on the BytespriteFactory's implementation. Then, the
            BytespriteFactory's implementation will return which sprite_sheet is supposed to be used. Finally, the
            ByteSprite's update function will take what is returned from the BytespriteFactory's method and assign
            the active_sheet to be what is returned. The two work in tandem.
    """

    active_sheet: list[pyg.Surface]  # The current spritesheet being used.
    spritesheets: list[list[pyg.Surface]]
    object_type: int
    rect: pyg.Rect
    screen: pyg.Surface
    image: pyg.Surface
    __frame_index: int  # Selects the sprite from the spritesheet to be used. Used for animation
    __config: Config = Config()
    __update_function: Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]]

    # make sure that all inherited classes constructors only take screen as a parameter
    def __init__(self, screen: pyg.Surface, filename: str, num_of_states: int, object_type: int,
                 update_function: Callable[[dict, int, Vector, list[list[pyg.Surface]]], list[pyg.Surface]],
                 colorkey: pyg.Color | None = None, top_left: Vector = Vector(0, 0)):
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
        """
        This method will start an animation based on the currently set active_sheet. Then, it will reassign the
        active_sheet based on what the BytespriteFactory's update method will return. Lastly, the
        ``set_image_and_render`` method is then called to display the new sprites in the active_sheet.
        :param data:
        :param layer:
        :param pos:
        :return: None
        """

        self.__frame_index = 0  # Starts the new spritesheet at the beginning
        self.rect.topleft = (
            pos.x * self.__config.TILE_SIZE * self.__config.SCALE + self.__config.GAME_BOARD_MARGIN_LEFT,
            pos.y * self.__config.TILE_SIZE * self.__config.SCALE + self.__config.GAME_BOARD_MARGIN_TOP)

        self.active_sheet = self.update_function(data, layer, pos, self.spritesheets)
        self.set_image_and_render()

    # Call this method at the end of the implemented logic and for each frame
    def set_image_and_render(self):
        """
        This method will take a single image from the current active_sheet and then display it on the screen.
        :return:
        """
        self.image = self.active_sheet[self.__frame_index]
        self.__frame_index = (self.__frame_index + 1) % self.__config.NUMBER_OF_FRAMES_PER_TURN
        self.screen.blit(self.image, self.rect)
