import random

from game.client.user_client import UserClient
from game.common.enums import *
from game.utils.vector import Vector


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
    
    def first_turn_init(self, world, avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.MINING
        self.base_position = self.find_all_by_type(world, self.my_station_type)[0]

    # This is where your AI will decide what to do
    def take_turn(self, turn: int, actions: ActionType, world, avatar):
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
            # actions = [ActionType.MOVE_LEFT if self.company == Company.TURING else ActionType.MOVE_RIGHT] # If I'm selling, move towards my base
            actions = self.generate_moves(avatar.position, self.base_position, turn % 2 == 0)
        else:
            if current_tile.occupied_by.object_type == ObjectType.ORE_OCCUPIABLE_STATION:
                # If I'm mining and I'm standing on an ore, mine it and set my state to selling
                actions = [ActionType.MINE]
                self.current_state = State.SELLING
            else:
                # If I'm mining and I'm not standing on an ore, move randomly
                actions = [random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_DOWN])]

        return actions

    def generate_moves(self, start_position, end_position, vertical_first):
        """
        This function will generate a path between the start and end position. It does not consider walls and will
        try to walk directly to the end position.
        :param start_position:      Position to start at
        :param end_position:        Position to get to
        :param vertical_first:      True if the path should be vertical first, False if the path should be horizontal first
        :return:                    Path represented as a list of ActionType
        """
        dx = end_position.x - start_position.x
        dy = end_position.y - start_position.y
        
        horizontal = [ActionType.MOVE_LEFT] * -dx if dx < 0 else [ActionType.MOVE_RIGHT] * dx
        vertical = [ActionType.MOVE_UP] * -dy if dy < 0 else [ActionType.MOVE_DOWN] * dy
        
        return vertical + horizontal if vertical_first else horizontal + vertical
    
    def find_all_by_type(self, world, object_type):
        """
        Finds all tiles on the board with the given object_type
        :param world:           Generic world information
        :param object_type:     The desired object type
        :return:                List of all Vectors for positions with Tiles with the object type
        """
        return self.find_all(world, lambda tile: tile.occupied_by is not None and tile.occupied_by.object_type == object_type)
    
    def find_all(self, world, criteria):
        """
        Finds all tiles on the board that match the given criteria
        :param world:           Generic world information
        :param criteria:        The required criteria as a function that takes a Tile and returns a bool
        :return:                List of all Vectors for positions with Tiles that meet the criteria
        """
        result = []
        for y in range(len(world.game_map)):
            for x in range(len(world.game_map[y])):
                if criteria(world.game_map[y][x]):
                    result.append(Vector(x=x, y=y))
        return result
