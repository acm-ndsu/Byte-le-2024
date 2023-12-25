from game.client.user_client import UserClient
from game.common.enums import *


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
        return 'The King\'s Lambdas 2'
    
    def first_turn_init(self, world, avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.MINING

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, avatar):
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
                actions = [ActionType.MOVE_RIGHT if self.company == Company.TURING else ActionType.MOVE_LEFT]
        
        return actions
