from copy import deepcopy
import random

from game.common.action import Action
from game.common.avatar import Avatar
from game.common.enums import *
from game.common.player import Player
import game.config as config   # this is for turns
from game.utils.thread import CommunicationThread
from game.controllers.movement_controller import MovementController
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController
from game.common.map.game_board import GameBoard
from game.config import MAX_NUMBER_OF_ACTIONS_PER_TURN


class MasterController(Controller):
    """
    give_client_objects:
        Takes a list of Player objects and places it in the game world.

    ----------------------------------------------------------------------------------------------------------------

    game_loop_logic:
        Increments the turn count as the game plays (look at the engine to see how it's controlled more).

    ----------------------------------------------------------------------------------------------------------------

    interpret_current_turn_data:
        This accesses the game_board in the first turn of the game and generates the game's seed.

    ----------------------------------------------------------------------------------------------------------------

    client_turn_arguments:
        There are lines of code commented out that create Action Objects instead of using the enum. If your project
        needs Actions Objects instead of the enums, comment out the enums and use Objects as necessary.

    ----------------------------------------------------------------------------------------------------------------

    turn_logic:
        This method executes every movement and interact behavior from every client in the game.

    ----------------------------------------------------------------------------------------------------------------

    create_turn_log:
        This method creates a dictionary that stores the turn, all client objects, and game_board's JSON file to
        be used as the turn log.

    ----------------------------------------------------------------------------------------------------------------

    return_final_results:
        This method creates a dictionary that stores a list of clients' JSON files. This represents the final
        results of the game.
    """
    def __init__(self):
        super().__init__()
        self.game_over: bool = False
        # self.event_timer = GameStats.event_timer   # anything related to events are commented it out until made
        # self.event_times: tuple[int, int] | None = None
        self.turn: int = 1
        self.current_world_data: dict = None
        self.movement_controller: MovementController = MovementController()
        self.interact_controller: InteractController = InteractController()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, clients: list[Player], world: dict):
        # starting_positions = [[3, 3], [3, 9]]   # would be done in generate game
        for index, client in enumerate(clients):
            client.avatar = Avatar(position=world[index])

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield str(self.turn)
            # Increment the turn counter by 1
            self.turn += 1

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, clients: list[Player], world: dict, turn):
        self.current_world_data = world
        if turn == 1:
            random.seed(world['game_board'].seed)
            # self.event_times = random.randrange(162, 172), random.randrange(329, 339)

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client: Player, turn):
        # turn_action: Action = Action()
        # client.action: Action = turn_action
        # ^if you want to use action as an object instead of an enum

        turn_actions: list[ActionType] | list = []
        client.actions = turn_actions

        # Create deep copies of all objects sent to the player
        current_world = deepcopy(self.current_world_data["game_board"])    # what is current world and copy avatar
        copy_avatar = deepcopy(client.avatar)
        # Obfuscate data in objects that that player should not be able to see
        # Currently world data isn't obfuscated at all
        args = (self.turn, turn_actions, current_world, copy_avatar)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients: list[Player], turn):
        for client in clients:
            for i in range(MAX_NUMBER_OF_ACTIONS_PER_TURN):
                self.movement_controller.handle_actions(client.actions[i], client, self.current_world_data["game_board"])
                self.interact_controller.handle_actions(client.actions[i], client, self.current_world_data["game_board"])
        # checks event logic at the end of round
        # self.handle_events(clients)

    # comment out for now, nothing is in place for event types yet
    # def handle_events(self, clients):
        # If it is time to run an event, master controller picks an event to run
        # if self.turn == self.event_times[0] or self.turn == self.event_times[1]:
        #    self.current_world_data["game_map"].generate_event(EventType.example, EventType.example)
        # event type.example is just a placeholder for now

    # Return serialized version of game
    def create_turn_log(self, clients: list[Player], turn: int):
        data = dict()
        data['tick'] = turn
        data['clients'] = [client.to_json() for client in clients]
        # Add things that should be thrown into the turn logs here
        data['game_board'] = self.current_world_data["game_board"].to_json()

        return data

    # Gather necessary data together in results file
    def return_final_results(self, clients: list[Player], turn):
        data = dict()

        data['players'] = list()
        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data
