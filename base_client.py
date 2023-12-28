import random

from game.client.user_client import UserClient
from game.common.enums import *
from game.utils.vector import Vector
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.map.tile import Tile
from typing import Callable


class State(Enum):
    MINING = auto()
    SELLING = auto()


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'The King\'s Lambdas 3'
    
    def first_turn_init(self, world: GameBoard, avatar: Avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.MINING

    # This is where your AI will decide what to do
    def take_turn(self, turn: int, actions: ActionType, world: GameBoard, avatar: Avatar):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        if turn == 1:
            self.first_turn_init(world, avatar)
            
        current_tile = world.game_map[avatar.position.y][avatar.position.x] # set current tile to the tile that I'm standing on
        
        # If I start the turn on my station, I should start mining
        if current_tile.occupied_by.object_type == self.my_station_type:
            self.current_state = State.MINING
            
        # Make action decision for this turn
        if self.current_state == State.SELLING:
            actions = [ActionType.MOVE_LEFT if self.company == Company.TURING else ActionType.MOVE_RIGHT] # If I'm selling, move towards my base
        else:
            if current_tile.occupied_by.object_type == ObjectType.ORE_OCCUPIABLE_STATION:
                # If I'm mining and I'm standing on an ore, mine it and set my state to selling
                actions = [ActionType.MINE]
                self.current_state = State.SELLING
            else:
                # If I'm mining and I'm not standing on an ore, move away from my station to try to find an ore
                actions = [random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_DOWN])]

        return actions

    def generate_moves(self, start_position: Vector, end_position: Vector, vertical_first: bool) -> [ActionType]:
        """
        This function will generate a path between the start and end position. It does not consider walls and will
        try to walk directly to the end position.
        :param start_position:      Position to start from
        :param end_position:        Position to get to
        :param vertical_first:      True if the path should be vertical first, False if the path should be horizontal first
        :return:                    Path represented as a list of ActionType
        """
        dx = end_position.x - start_position.x
        dy = end_position.y - start_position.y
        
        horizontal = [ActionType.MOVE_LEFT] * -dx if dx < 0 else [ActionType.MOVE_RIGHT] * dx
        vertical = [ActionType.MOVE_UP] * -dy if dy < 0 else [ActionType.MOVE_DOWN] * dy
        
        return vertical + horizontal if vertical_first else horizontal + vertical
    
    def find_all_by_type(self, world: GameBoard, object_type: ObjectType) -> [Tile]:
        """
        Finds all tiles on the board with the given object_type
        :param world:           Generic world information
        :param object_type:     The desired object type
        :return:                List of all tiles with the object type
        """
        return self.find_all(world, lambda tile: tile.occupied_by.object_type == object_type)
    
    def find_all(self, world: GameBoard, criteria: Callable[[Tile], bool]) -> [Tile]:
        """
        Finds all tiles on the board that match the given criteria
        :param world:           Generic world information
        :param criteria:        The required criteria as a function from a Tile to a bool
        :return:                List of all tiles that meet the criteria
        """
        tiles = [tile for row in world.game_map for tile in row]
        return [tile for tile in tiles if criteria(tile)]
