import math
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import cv2

import game.config
from typing import Callable
from game.utils.vector import Vector
from visualizer.adapter import Adapter
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.config import Config
from visualizer.utils.log_reader import logs_to_dict
from visualizer.templates.playback_template import PlaybackButtons
from threading import Thread


class ByteVisualiser:

    def __init__(self, end_time: int = -1, skip_start: bool = False, playback_speed: float = 1.0,
                 fullscreen: bool = False,
                 save_video: bool = False, loop_count: int = 1, turn_start: int = 0, turn_end: int = -1,
                 log_dir: str | None = None):
        pygame.init()
        self.logs = log_dir
        self.config: Config = Config()
        self.turn_logs: dict[str:dict] = {}
        self.size: Vector = self.config.SCREEN_SIZE
        self.tile_size: int = self.config.TILE_SIZE

        self.fullscreen: bool = fullscreen
        self.screen: pygame.Surface = pygame.display.set_mode(self.size.as_tuple(),
                                                              pygame.FULLSCREEN if self.fullscreen else pygame.SHOWN)
        self.adapter: Adapter = Adapter(self.screen)

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.tick: int = turn_start * self.config.NUMBER_OF_FRAMES_PER_TURN
        self.turn_end: int = turn_end
        self.bytesprite_factories: dict[int: Callable[[pygame.Surface], ByteSprite]] = {}
        self.bytesprite_map: [[[ByteSprite]]] = list()

        self.default_frame_rate: int = self.config.FRAME_RATE

        self.playback_speed: float = playback_speed
        self.paused: bool = False
        self.recording: bool = save_video

        # Scale for video saving (division can be adjusted, higher division = lower quality)
        self.scaled: tuple[int, int] = (self.size.x // 2, self.size.y // 2)
        self.writer: cv2.VideoWriter = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'mp4v'),
                                                       self.default_frame_rate, self.scaled)
        self.end_time: int = end_time
        self.skip_start: bool = skip_start
        self.loop_count: int = loop_count

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, config: Config) -> None:
        if config is None or not isinstance(config, Config):
            # Error messaging should look like the message below going forward
            raise ValueError(
                f'{self.__class__.__name__}.config must be a Config. It is a(n) {type(config)} with the value of {config}')
        self.__config: Config = config

    @property
    def turn_logs(self) -> dict[str:dict]:
        return self.__turn_logs

    @turn_logs.setter
    def turn_logs(self, turn_logs: dict[str:dict]) -> None:
        if turn_logs is None or not isinstance(turn_logs, dict):
            raise ValueError(
                f'{self.__class__.__name__}.turn_logs must be a dict. It is a(n) {type(turn_logs)} with the value of {turn_logs}')
        self.__turn_logs: dict = turn_logs

    @property
    def size(self) -> Vector:
        return self.__size

    @size.setter
    def size(self, size: Vector) -> None:
        if size is None or not isinstance(size, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.size must be a Vector. It is a(n) {type(size)} with the value of {size}')
        self.__size: Vector = size

    @property
    def tile_size(self) -> int:
        return self.__tile_size

    @tile_size.setter
    def tile_size(self, tile_size: int) -> None:
        if tile_size is None or not isinstance(tile_size, int):
            raise ValueError(
                f'{self.__class__.__name__}.tile_size must be an int. It is a(n) {type(tile_size)} with the value of {tile_size}')
        self.__tile_size: int = tile_size

    @property
    def fullscreen(self) -> bool:
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, fullscreen: bool) -> None:
        if fullscreen is None or not isinstance(fullscreen, bool):
            raise ValueError(
                f'{self.__class__.__name__}.fullscreen must be a bool. It is a(n) {type(fullscreen)} with the value of {fullscreen}')
        self.__fullscreen: bool = fullscreen

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        if screen is None or not isinstance(screen, pygame.Surface):
            raise ValueError(
                f'{self.__class__.__name__}.screen must be a pygame.Surface. It is a(n) {type(screen)} with the value of {screen}')
        self.__screen: pygame.Surface = screen

    @property
    def adapter(self) -> Adapter:
        return self.__adapter

    @adapter.setter
    def adapter(self, adapter: Adapter) -> None:
        if adapter is None or not isinstance(adapter, Adapter):
            raise ValueError(
                f'{self.__class__.__name__}.adapter must be an Adapter. It is a(n) {type(adapter)} with the value of {adapter}')
        self.__adapter: Adapter = adapter

    @property
    def clock(self) -> pygame.time.Clock:
        return self.__clock

    @clock.setter
    def clock(self, clock: pygame.time.Clock) -> None:
        if clock is None or not isinstance(clock, pygame.time.Clock):
            raise ValueError(
                f'{self.__class__.__name__}.clock must be a pygame.time.Clock. It is a(n) {type(clock)} with the value of {clock}')
        self.__clock: pygame.time.Clock = clock

    @property
    def tick(self) -> int:
        return self.__tick

    @tick.setter
    def tick(self, tick: int) -> None:
        if tick is None or not isinstance(tick, int):
            raise ValueError(
                f'{self.__class__.__name__}.tick must be an int. It is a(n) {type(tick)} with the value of {tick}')
        self.__tick: int = tick

    @property
    def turn_end(self) -> int:
        return self.__turn_end

    @turn_end.setter
    def turn_end(self, turn_end: int) -> None:
        if turn_end is None or not isinstance(turn_end, int):
            raise ValueError(
                f'{self.__class__.__name__}.turn_end must be an int. It is a(n) {type(turn_end)} with the value of {turn_end}')
        self.__turn_end: int = turn_end

    @property
    def bytesprite_factories(self) -> dict[int: Callable[[pygame.Surface], ByteSprite]]:
        return self.__bytesprite_factories

    @bytesprite_factories.setter
    def bytesprite_factories(self, bytesprite_factories: dict) -> None:
        if bytesprite_factories is None or not isinstance(bytesprite_factories, dict):
            raise ValueError(
                f'{self.__class__.__name__}.bytesprite_factories must be a dict. It is a(n) {type(bytesprite_factories)} with the value of {bytesprite_factories}')
        self.__bytesprite_factories: dict = bytesprite_factories

    @property
    def bytesprite_map(self) -> list:
        return self.__bytesprite_map

    @bytesprite_map.setter
    def bytesprite_map(self, bytesprite_map: list) -> None:
        if bytesprite_map is None or not isinstance(bytesprite_map, list):
            raise ValueError(
                f'{self.__class__.__name__}.bytesprite_map must be a list. It is a(n) {type(bytesprite_map)} with the value of {bytesprite_map}')
        self.__bytesprite_map: list = bytesprite_map

    @property
    def default_frame_rate(self) -> int:
        return self.__default_frame_rate

    @default_frame_rate.setter
    def default_frame_rate(self, default_frame_rate: int) -> None:
        if default_frame_rate is None or not isinstance(default_frame_rate, int):
            raise ValueError(
                f'{self.__class__.__name__}.default_frame_rate must be an int. It is a(n) {type(default_frame_rate)} with the value of {default_frame_rate}')
        self.__default_frame_rate: int = default_frame_rate

    @property
    def playback_speed(self) -> float:
        return self.__playback_speed

    @playback_speed.setter
    def playback_speed(self, playback_speed: float) -> None:
        if playback_speed is None or not isinstance(playback_speed, float) or playback_speed < 1:
            raise ValueError(
                f'{self.__class__.__name__}.playback_speed must be a float greater than or equal to 1.0. It is a(n) {type(playback_speed)} with the value of {playback_speed}.')
        self.__playback_speed: float = playback_speed

    @property
    def paused(self) -> bool:
        return self.__paused

    @paused.setter
    def paused(self, paused: bool) -> None:
        if paused is None or not isinstance(paused, bool):
            raise ValueError(
                f'{self.__class__.__name__}.paused must be a bool. It is a(n) {type(paused)} with the value of {paused}')
        self.__paused: bool = paused

    @property
    def recording(self) -> bool:
        return self.__recording

    @recording.setter
    def recording(self, recording: bool) -> None:
        if recording is None or not isinstance(recording, bool):
            raise ValueError(
                f'{self.__class__.__name__}.recording must be a bool. It is a(n) {type(recording)} with the value of {recording}')
        self.__recording: bool = recording

    @property
    def scaled(self) -> tuple[int, int]:
        return self.__scaled

    @scaled.setter
    def scaled(self, scaled: tuple[int, int]) -> None:
        if scaled is None or not isinstance(scaled, tuple) or len(scaled) != 2 or any(
                map(lambda x: not isinstance(x, int), scaled)):
            raise ValueError(
                f'{self.__class__.__name__}.scaled must be a tuple[int, int]. It is a(n) {type(scaled)} with the value of {scaled}')
        self.__scaled: tuple[int, int] = scaled

    @property
    def writer(self) -> cv2.VideoWriter:
        return self.__writer

    @writer.setter
    def writer(self, writer: cv2.VideoWriter) -> None:
        if writer is None or not isinstance(writer, cv2.VideoWriter):
            raise ValueError(
                f'{self.__class__.__name__}.writer must be an cv2.VideoWriter. It is a(n) {type(writer)} with the value of {writer}')
        self.__writer: cv2.VideoWriter = writer

    @property
    def end_time(self) -> int:
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time: int) -> None:
        if end_time is None or not isinstance(end_time, int):
            raise ValueError(
                f'{self.__class__.__name__}.end_time must be an int. It is a(n) {type(end_time)} with the value of {end_time}')
        self.__end_time: int = end_time

    @property
    def skip_start(self) -> bool:
        return self.__skip_start

    @skip_start.setter
    def skip_start(self, skip_start: bool) -> None:
        if skip_start is None or not isinstance(skip_start, bool):
            raise ValueError(
                f'{self.__class__.__name__}.skip_start must be a bool. It is a(n) {type(skip_start)} with the value of {skip_start}')
        self.__skip_start: bool = skip_start

    @property
    def loop_count(self) -> int:
        return self.__loop_count

    @loop_count.setter
    def loop_count(self, loop_count: int) -> None:
        if loop_count is None or not isinstance(loop_count, int):
            raise ValueError(
                f'{self.__class__.__name__}.loop_count must be an int. It is a(n) {type(loop_count)} with the value of {loop_count}')
        self.__loop_count: int = loop_count


    def load(self) -> None:
        self.turn_logs: dict = logs_to_dict(self.logs)
        self.bytesprite_factories = self.adapter.populate_bytesprite_factories()


    def prerender(self) -> None:
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.adapter.prerender()

    def render(self, button_pressed: PlaybackButtons) -> bool:
        # Run playback buttons method
        self.__playback_controls(button_pressed)

        if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0:
            # NEXT TURN
            turn: int = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN+1
            if self.turn_logs.get(f'turn_{turn:04d}') is None or \
                    (self.turn_end != -1 and turn == self.turn_end):
                return False
            self.recalc_animation(self.turn_logs[f'turn_{turn:04d}'])
            self.adapter.recalc_animation(
                self.turn_logs[f'turn_{turn:04d}'])

        else:
            # NEXT ANIMATION FRAME
            self.continue_animation()
            self.adapter.continue_animation()

        self.adapter.render()
        pygame.display.flip()

        # If recording, save frames into video
        if self.recording:
            self.save_video()
            # Reduce ticks to just one frame per turn for saving video (can be adjusted)
            self.tick += self.config.NUMBER_OF_FRAMES_PER_TURN - 1
        self.tick += 1
        return True

    # Method to deal with playback_controls in visualizer ran in render method
    def __playback_controls(self, button_pressed: PlaybackButtons) -> None:
        # If recording, do not allow button to work
        if not self.recording:
            # Save button
            if PlaybackButtons.SAVE_BUTTON in button_pressed:
                self.recording = True
                self.playback_speed = 10.0
                self.tick = 0
            if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0 and self.paused:
                self.tick = max(self.tick - self.config.NUMBER_OF_FRAMES_PER_TURN, 0)
            # Prev button to go back a frame
            if PlaybackButtons.PREV_BUTTON in button_pressed:
                turn = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN
                self.tick = (turn - 1) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Next button to go forward a frame
            if PlaybackButtons.NEXT_BUTTON in button_pressed:
                turn = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN
                self.tick = (turn + 1) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Start button to restart visualizer
            if PlaybackButtons.START_BUTTON in button_pressed:
                self.tick = 0
            # End button to end visualizer
            if PlaybackButtons.END_BUTTON in button_pressed:
                self.tick = self.config.NUMBER_OF_FRAMES_PER_TURN * (game.config.MAX_TICKS + 1)
            # Pause button to pause visualizer (allow looping of turn animation)
            if PlaybackButtons.PAUSE_BUTTON in button_pressed:
                self.paused = not self.paused
            if PlaybackButtons.NORMAL_SPEED_BUTTON in button_pressed:
                self.playback_speed = 1.0
            if PlaybackButtons.FAST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 2.0
            if PlaybackButtons.FASTEST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 4.0

    # Method to deal with saving game to mp4 (called in render if save button pressed)
    def save_video(self) -> None:
        # Convert to PIL Image
        new_image = pygame.surfarray.pixels3d(self.screen.copy())
        # Rotate ndarray
        new_image = new_image.swapaxes(1, 0)
        # shrink size for recording
        new_image = cv2.resize(new_image, self.scaled)
        # Convert to OpenCV Image with numpy
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGR)
        # Write image and go to next turn
        self.writer.write(new_image)

    def recalc_animation(self, turn_data: dict) -> None:
        """
        Determine what bytesprites are needed at which location and calls logic to determine active spritesheet and render
        :param turn_data: A dictionary of all the turn data for current turn
        :return: None
        """
        game_map: [[dict]] = turn_data['game_board']['game_map']
        # Iterate on each row on the game map
        row: list
        for y, row in enumerate(game_map):
            # Add rows to bytesprite_map if needed
            self.__add_rows(y)
            # Iterate on each tile in the row
            tile: dict
            for x, tile in enumerate(row):
                # Add tiles to row if needed
                if len(self.bytesprite_map[y]) < x + 1:
                    self.bytesprite_map[y].append(list())
                # Render layers on tile
                temp_tile: dict | None = tile
                z: int = 0
                while temp_tile is not None:
                    # Add layers if needed
                    self.__add_needed_layers(x, y, z)

                    # Create or replace bytesprite at current tile on this current layer
                    self.__create_bytesprite(x, y, z, temp_tile)

                    # Call render logic on bytesprite
                    self.bytesprite_map[y][x][z].update(temp_tile, z, Vector(y=y, x=x))
                    # increase iteration
                    temp_tile = temp_tile.get('occupied_by') if temp_tile.get('occupied_by') is not None \
                        else (temp_tile.get('held_item') if self.config.VISUALIZE_HELD_ITEMS
                              else None)
                    z += 1

                # clean up additional layers
                self.__clean_up_layers(x, y, z)

    # Add rows to bytesprite_map ran in recalc_animation method
    def __add_rows(self, y: int) -> None:
        if len(self.bytesprite_map) < y + 1:
            self.bytesprite_map.append(list())

    # Add layers ran in recalc_animation method
    def __add_needed_layers(self, x: int, y: int, z: int) -> None:
        if len(self.bytesprite_map[y][x]) < z + 1:
            self.bytesprite_map[y][x].append(None)

    # Create bytesprite at current tile ran in recalc_animation method
    def __create_bytesprite(self, x: int, y: int, z: int, temp_tile: dict | None) -> None:
        if self.bytesprite_map[y][x][z] is None or \
                self.bytesprite_map[y][x][z].object_type != temp_tile['object_type']:
            if len(self.bytesprite_factories) == 0:
                raise ValueError(f'must provide bytesprite factories for visualization!')
            # Check that a bytesprite template exists for current object type
            factory_function: Callable[[pygame.Surface], ByteSprite] | None = self.bytesprite_factories.get(
                temp_tile['object_type'])
            if factory_function is None:
                raise ValueError(
                    f'Must provide a bytesprite for each object type! Missing object_type: {temp_tile["object_type"]}')

            # Instantiate a new bytesprite on current layer
            self.bytesprite_map[y][x][z] = factory_function(self.screen)

    # Additional layer clean up method ran in recalc_animation method
    def __clean_up_layers(self, x: int, y: int, z: int) -> None:
        while len(self.bytesprite_map[y][x]) > z:
            self.bytesprite_map[y][x].pop()

    def continue_animation(self) -> None:
        row: list
        tile: list
        sprite: ByteSprite
        [sprite.set_image_and_render() for row in self.bytesprite_map for tile in row for sprite in tile]

    def postrender(self) -> None:
        self.adapter.clean_up()
        self.clock.tick(self.default_frame_rate * self.playback_speed)

    def loop(self) -> None:
        for _ in range(self.loop_count):
            thread: Thread = Thread(target=self.load)
            thread.start()

            # Start Menu loop
            in_phase: bool = True
            if not self.skip_start:
                self.__start_menu_loop(in_phase)

            thread.join()

            # Playback Menu loop
            in_phase = True
            self.__play_back_menu_loop(in_phase)

            # Results
            in_phase = True
            self.__results_loop(in_phase)

        if self.recording:
            self.writer.release()

        sys.exit()

    # Start menu loop ran in loop method
    def __start_menu_loop(self, in_phase: bool) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.start_menu_event(event)

            self.adapter.start_menu_render()

            pygame.display.flip()

            if not in_phase:
                break
            self.clock.tick(self.default_frame_rate * self.playback_speed)

    # Playback menu loop ran in loop method
    def __play_back_menu_loop(self, in_phase: bool) -> None:
        while True:
            playback_buttons: PlaybackButtons = PlaybackButtons(0)
            # pygame events used to exit the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                playback_buttons = self.adapter.on_event(event)

            self.prerender()

            if in_phase:
                in_phase = self.render(playback_buttons)

            if not in_phase:
                break
            self.postrender()

    # Results loop method ran in loop method
    def __results_loop(self, in_phase: bool) -> None:
        self.adapter.results_load(self.turn_logs['results'])
        ticks: int = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.results_event(event)

            self.adapter.results_render()

            pygame.display.flip()

            if self.recording:
                self.save_video()

            if not in_phase or (self.end_time != -1 and ticks >= self.end_time * math.floor(
                    self.default_frame_rate * self.playback_speed)):
                break
            self.clock.tick(math.floor(self.default_frame_rate * self.playback_speed))
            ticks += 1
        self.writer.release()


if __name__ == '__main__':
    byte_visualiser: ByteVisualiser = ByteVisualiser()
    byte_visualiser.loop()
