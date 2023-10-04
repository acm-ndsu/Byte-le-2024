from game.utils.vector import Vector


class Config:
    __NUMBER_OF_FRAMES_PER_TURN: int = 4
    __TILE_SIZE: int = 16
    __SCALE: int = 5
    __SCREEN_SIZE: Vector = Vector(x=1366, y=768)  # width, height
    __FRAME_RATE: int = 12
    __BACKGROUND_COLOR: (int, int, int) = 0, 0, 0
    __GAME_BOARD_MARGIN_LEFT: int = 440
    __GAME_BOARD_MARGIN_TOP: int = 100
    __VISUALIZE_HELD_ITEMS: bool = True

    # if you have an animation, this will be the number of frames the animation goes through for each turn
    @property
    def NUMBER_OF_FRAMES_PER_TURN(self) -> int:
        return self.__NUMBER_OF_FRAMES_PER_TURN

    # this will be the size of the tile-its going to be squares
    @property
    def TILE_SIZE(self) -> int:
        return self.__TILE_SIZE

    # scale is for the tile size being scaled larger,
    # for ex: if you have a 16x16 tile, we can scale it to 4 so it looks larger
    @property
    def SCALE(self) -> int:
        return self.__SCALE

    # the screen size is the overall screen size
    @property
    def SCREEN_SIZE(self) -> Vector:
        return self.__SCREEN_SIZE

    # frame rate is the overall frame rate
    @property
    def FRAME_RATE(self) -> int:
        return self.__FRAME_RATE

    # this is where you can set the default background color
    @property
    def BACKGROUND_COLOR(self) -> (int, int, int):
        return self.__BACKGROUND_COLOR

    @property
    def GAME_BOARD_MARGIN_LEFT(self) -> int:
        return self.__GAME_BOARD_MARGIN_LEFT

    @property
    def GAME_BOARD_MARGIN_TOP(self) -> int:
        return self.__GAME_BOARD_MARGIN_TOP

    @property
    def VISUALIZE_HELD_ITEMS(self) -> bool:
        return self.__VISUALIZE_HELD_ITEMS



