import math
import sys
import os

import numpy
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

    def __init__(self):
        pygame.init()
        self.config: Config = Config()
        self.turn_logs: dict[str:dict] = {}
        self.size: Vector = self.config.SCREEN_SIZE
        self.tile_size: int = self.config.TILE_SIZE

        self.screen: pygame.display = pygame.display.set_mode(self.size.as_tuple())
        self.adapter: Adapter = Adapter(self.screen)

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.tick: int = 0
        self.bytesprite_factories: dict[int: Callable[[pygame.Surface], ByteSprite]] = {}
        self.bytesprite_map: [[[ByteSprite]]] = list()

        self.default_frame_rate: int = self.config.FRAME_RATE

        self.playback_speed: int = 1
        self.paused: bool = False
        self.recording: bool = False

        # Scale for video saving (division can be adjusted, higher division = lower quality)
        self.scaled: tuple[int, int] = (self.size.x // 2, self.size.y // 2)
        self.writer: cv2.VideoWriter

    def load(self) -> None:
        self.turn_logs: dict = logs_to_dict()
        self.bytesprite_factories = self.adapter.populate_bytesprite_factories()

    def prerender(self) -> None:
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.adapter.prerender()

    def render(self, button_pressed: PlaybackButtons) -> bool:
        # Run playback buttons method
        self.__playback_controls(button_pressed)

        if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0:
            # NEXT TURN
            if self.turn_logs.get(f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}') is None:
                return False
            self.recalc_animation(self.turn_logs[f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}'])
            self.adapter.recalc_animation(
                self.turn_logs[f'turn_{self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1:04d}'])

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
                self.writer = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'mp4v'),
                                              self.default_frame_rate, self.scaled)
                self.playback_speed = 10
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
                self.playback_speed = 1
            if PlaybackButtons.FAST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 2
            if PlaybackButtons.FASTEST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 4

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
        thread: Thread = Thread(target=self.load)
        thread.start()

        # Start Menu loop
        in_phase: bool = True
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

            self.screen.fill(self.config.BACKGROUND_COLOR)

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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.results_event(event)

            self.screen.fill(self.config.BACKGROUND_COLOR)

            self.adapter.results_render()

            pygame.display.flip()

            if self.recording:
                self.save_video()

            if not in_phase:
                break

            self.clock.tick(math.floor(self.default_frame_rate * self.playback_speed))

        if self.recording:
            self.writer.release()


if __name__ == '__main__':
    byte_visualiser: ByteVisualiser = ByteVisualiser()
    byte_visualiser.loop()
