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
        return 'Volunteer'

    def first_turn_init(self, world, avatar):
        """
        This is where you can put setup for things that should happen at the beginning of the first turn
        """
        self.company = avatar.company
        self.my_station_type = ObjectType.TURING_STATION if self.company == Company.TURING else ObjectType.CHURCH_STATION
        self.current_state = State.MINING
        self.base_position = world.get_objects(self.my_station_type)[0][0]

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

        current_tile = world.game_map[avatar.position.y][
            avatar.position.x]  # set current tile to the tile that I'm standing on

        # If I start the turn on my station, I should...
        if current_tile.occupied_by.object_type == self.my_station_type:
            # buy Improved Mining tech if I can...
            if avatar.science_points >= avatar.get_tech_info('Improved Drivetrain').cost and not avatar.is_researched(
                    'Improved Drivetrain'):
                return [ActionType.BUY_IMPROVED_DRIVETRAIN]
            # otherwise set my state to mining
            self.current_state = State.MINING

        # If I have at least 5 items in my inventory, set my state to selling
        if len([item for item in self.get_my_inventory(world) if item is not None]) >= 5:
            self.current_state = State.SELLING

        # Make action decision for this turn
        if self.current_state == State.SELLING:
            # actions = [ActionType.MOVE_LEFT if self.company == Company.TURING else ActionType.MOVE_RIGHT] # If I'm selling, move towards my base
            actions = self.generate_moves(avatar.position, self.base_position, turn % 2 == 0)
        else:
            if current_tile.occupied_by.object_type == ObjectType.ORE_OCCUPIABLE_STATION:
                # If I'm mining and I'm standing on an ore, mine it
                actions = [ActionType.MINE]
            else:
                # If I'm mining and I'm not standing on an ore, move randomly
                actions = [random.choice(
                    [ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_DOWN])]

        return actions

    def determine_tech_buy(self, avatar):
        if not avatar.is_researched('Improved Mining'):
            info = avatar.get_tech_info('Improved Mining')
            if avatar.science_points >= info.cost:
                return [ActionType.BUY_IMPROVED_MINING]

        elif not avatar.is_researched('Improved Drivetrain'):
            info = avatar.get_tech_info('Improved Drivetrain')
            if avatar.science_points >= info.cost:
                return [ActionType.BUY_IMPROVED_DRIVETRAIN]

        elif not avatar.is_researched('Superior Mining'):
            info = avatar.get_tech_info('Superior Mining')
            if avatar.science_points >= info.cost:
                return [ActionType.BUY_SUPERIOR_MINING]

        elif not avatar.is_researched('Superior Drivetrain'):
            info = avatar.get_tech_info('Superior Drivetrain')
            if avatar.science_points >= info.cost:
                return [ActionType.BUY_SUPERIOR_DRIVETRAIN]

        elif not avatar.is_researched('Dynamite'):
            info = avatar.get_tech_info('Dynamite')
            if avatar.science_points >= info.cost:
                return [ActionType.BUY_DYNAMITE]

        return []

    def distance(self, pos_1, pos_2, world):
        return len(self.find_path(pos_1, pos_2, world))

    def find_path(self, start, goal, world):
        start = (start.y, start.x)
        goal = (goal.y, goal.x)
        h = lambda pos: abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        def reconstruct_path(came_through, current):
            total_path = [current]
            while current in came_through.keys():
                current = came_through[current]
                total_path = [current] + total_path
            return total_path

        def to_actions(poses):
            result = []
            for i in range(len(poses) - 1):
                if poses[i + 1][0] > poses[i][0]:
                    result.append(ActionType.MOVE_DOWN)
                if poses[i + 1][0] < poses[i][0]:
                    result.append(ActionType.MOVE_UP)
                if poses[i + 1][1] > poses[i][1]:
                    result.append(ActionType.MOVE_RIGHT)
                if poses[i + 1][1] < poses[i][1]:
                    result.append(ActionType.MOVE_LEFT)
            return result

        def neighbors(pos):
            return list(filter(lambda p: p[0] in range(0, 14) and p[1] in range(0, 14) and (
                        world.game_map[pos[0]][pos[1]].occupied_by is None or world.game_map[pos[0]][
                    pos[1]].occupied_by.object_type != ObjectType.WALL),
                               [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1),
                                (pos[0], pos[1] - 1)]))

        looking_set = {start}

        came_through = {}

        g_score = {}
        g_score[start] = 0

        f_score = {}
        f_score[start] = h(start)

        def get_f_score(pos):
            return f_score[pos] if pos in f_score.keys() else 999999999  # f score is infinity if it isn't already set

        while len(looking_set) != 0:
            current = None
            for pos in looking_set:
                if current is None or get_f_score(pos) < get_f_score(current):
                    current = pos
            if current == goal:
                return to_actions(reconstruct_path(came_through, current))

            looking_set.remove(current)
            for neighbor in neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score.keys() or tentative_g_score < g_score[neighbor]:
                    came_through[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h(neighbor)
                    if neighbor not in looking_set:
                        looking_set.add(neighbor)

        return []

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

    def get_my_inventory(self, world):
        return [item for item in world.inventory_manager.get_inventory(self.company) if item is not None]
