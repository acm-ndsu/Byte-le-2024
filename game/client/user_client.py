from game.common.enums import *
from game.config import Debug
import logging


class UserClient:
    def __init__(self):
        self.debug_level = DebugLevel.CLIENT
        self.debug = True

    def debug(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            logging.basicConfig(level=logging.DEBUG)
            for arg in args:
                logging.debug(f'{self.__class__.__name__}: {arg}')

    def team_name(self):
        return "No_Team_Name_Available"

    def take_turn(self, turn, actions, world, avatar):
        raise NotImplementedError("Implement this in subclass")
