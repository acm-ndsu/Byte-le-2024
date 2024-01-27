import random

from game.client.user_client import UserClient
from game.common.avatar import Avatar
from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.utils.vector import Vector


def heuristic(node: Vector, goal: Vector) -> int:
    return abs(node.x - goal.x) + abs(node.y - goal.y)


def construct_path(node: Vector, came_from: dict[Vector, Vector]) -> list[Vector]:
    path = [node]
    while node in came_from:
        node = came_from[node]
        path.append(node)

    return path[::-1]


def to_actions(path: list[Vector]) -> list[ActionType]:
    action_map: dict[Vector, ActionType] = {
        Vector(1): ActionType.MOVE_RIGHT,
        Vector(-1): ActionType.MOVE_LEFT,
        Vector(y=1): ActionType.MOVE_DOWN,
        Vector(y=-1): ActionType.MOVE_UP
    }
    if len(path) < 2:
        return []
    return [action_map[step - current] for current, step in zip(path, path[1:])]


def get_neighbours(node: Vector, game_state: GameBoard) -> list[Vector]:
    neighbours = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    return [node + Vector(dx, dy) for dx, dy in neighbours
            if not game_state.game_map[node.y + dy][node.x + dx].is_occupied_by_game_object(Wall)
            and not game_state.game_map[node.y + dy][node.x + dx].is_occupied_by_game_object(Avatar)]


def find_path(start: Vector, goal: Vector, game_state: GameBoard) -> list[Vector]:
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return []

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = get_neighbours(node, game_state)
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in [n for n in neighbours if n not in path]:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)


def get_closest_ore(node: Vector, game_state: GameBoard) -> Vector:
    return min([x[0] for x in game_state.get_objects(ObjectType.ORE_OCCUPIABLE_STATION)],
               key=lambda x: heuristic(x, node))


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
        return 'The Real Jean'

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
            if avatar.science_points >= avatar.get_tech_info('Improved Mining').cost and not avatar.is_researched(
                    'Improved Mining'):
                return [ActionType.BUY_IMPROVED_MINING]
            if avatar.science_points >= avatar.get_tech_info(Tech.DYNAMITE).cost and not avatar.is_researched(
                    Tech.DYNAMITE) and avatar.is_researched(Tech.IMPROVED_MINING):
                return [ActionType.BUY_DYNAMITE]
            if avatar.science_points >= avatar.get_tech_info('Superior Drivetrain').cost and not avatar.is_researched(
                    'Superior Drivetrain') and avatar.is_researched('Improved Drivetrain'):
                return [ActionType.BUY_SUPERIOR_DRIVETRAIN]
            if avatar.science_points >= avatar.get_tech_info('Superior Mining').cost and not avatar.is_researched(
                    'Superior Mining') and avatar.is_researched('Improved Mining'):
                return [ActionType.BUY_SUPERIOR_MINING]
            if avatar.science_points >= avatar.get_tech_info('Overdrive Drivetrain').cost and not avatar.is_researched(
                    'Overdrive Drivetrain') and avatar.is_researched('Superior Drivetrain'):
                return [ActionType.BUY_OVERDRIVE_DRIVETRAIN]
            if avatar.science_points >= avatar.get_tech_info('Overdrive Mining').cost and not avatar.is_researched(
                    'Overdrive Mining') and avatar.is_researched('Superior Mining'):
                return [ActionType.BUY_OVERDRIVE_MINING]

            # otherwise set my state to mining
            self.current_state = State.MINING

        # If I have at least 5 items in my inventory, set my state to selling
        if len([item for item in self.get_my_inventory(world) if item is not None]) >= 40:
            self.current_state = State.SELLING

        # Make action decision for this turn
        if self.current_state == State.SELLING:
            actions = to_actions(find_path(avatar.position, self.base_position, world))
        else:
            if current_tile.occupied_by.object_type == ObjectType.ORE_OCCUPIABLE_STATION:
                # If I'm mining and I'm standing on an ore, mine it
                actions = [ActionType.MINE]
            elif avatar.can_place_dynamite():
                actions = [ActionType.PLACE_DYNAMITE]
            else:
                try:
                    actions = to_actions(find_path(avatar.position, get_closest_ore(avatar.position, world), world))
                except:
                    # If I'm mining and I'm not standing on an ore, move randomly
                    self.current_state = State.SELLING
                    actions = [random.choice(
                        [ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_DOWN])]

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

    def get_my_inventory(self, world):
        return world.inventory_manager.get_inventory(self.company)
