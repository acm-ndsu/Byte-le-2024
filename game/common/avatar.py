from typing import Self

from game.common.enums import ObjectType, Company
from game.common.game_object import GameObject
from game.quarry_rush.tech.tech import TechInfo
from game.utils.vector import Vector
from game.quarry_rush.tech.tech_tree import TechTree
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions
from game.quarry_rush.dynamite_active_ability import DynamiteActiveAbility


class Avatar(GameObject):

    def __init__(self, company: Company = Company.CHURCH, position: Vector | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.score: int = 0
        self.science_points: int = 0
        self.position: Vector | None = position
        self.movement_speed: int = 1  # determines how many tiles the player moves
        self.drop_rate: float = 1.0  # determines how many items are dropped after mining
        self.__abilities: dict = self.__create_abilities_dict()  # used to manage unlocking new abilities
        self.__tech_tree: TechTree = self.__create_tech_tree()  # the tech tree cannot be set; made private for security
        self.__company: Company = company
        self.dynamite_active_ability: DynamiteActiveAbility = DynamiteActiveAbility()
        self.placing_trap: bool = False
        self.placing_dynamite: bool = False

    @property
    def company(self) -> Company:
        return self.__company

    @property
    def score(self) -> int:
        return self.__score

    @property
    def science_points(self) -> int:
        return self.__science_points

    @property
    def position(self) -> Vector | None:
        return self.__position

    @property
    def movement_speed(self):
        return self.__movement_speed

    @property
    def drop_rate(self):
        return self.__drop_rate

    @company.setter
    def company(self, company: Company) -> None:
        self.__company = company

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(f'{self.__class__.__name__}.score must be an int.')

        if score < 0:
            raise ValueError(f'{self.__class__.__name__}.score must be a positive int.')

        self.__score: int = score

    @science_points.setter
    def science_points(self, points: int) -> None:
        if points is None or not isinstance(points, int):
            raise ValueError(f'{self.__class__.__name__}.science_points must be an int.')

        if points < 0:
            raise ValueError(f'{self.__class__.__name__}.science_points must be a positive int.')

        self.__science_points: int = points

    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None.')
        self.__position: Vector | None = position

    @movement_speed.setter
    def movement_speed(self, speed: int) -> None:
        if speed is None or not isinstance(speed, int):
            raise ValueError(f'{self.__class__.__name__}.movement_speed must be an int.')

        if speed < 0:
            raise ValueError(f'{self.__class__.__name__}.movement_speed must be a positive int.')

        self.__movement_speed: int = speed

    @drop_rate.setter
    def drop_rate(self, drop_rate: float) -> None:
        if drop_rate is None or not isinstance(drop_rate, float):
            raise ValueError(f'{self.__class__.__name__}.drop_rate must be a float.')

        if drop_rate < 0:
            raise ValueError(f'{self.__class__.__name__}.drop_rate must be a positive float.')

        self.__drop_rate = drop_rate

    # Tech Tree methods and implementation------------------------------------------------------------------------------

    # Helper method to create the tech tree
    def __create_tech_tree(self) -> TechTree:
        avatar_functions = AvatarFunctions(increase_movement=self.__increase_movement,  # change number for balance
                                           increase_mining=self.__increase_drop_rate,  # change number for balance
                                           unlock_movement_overdrive=self.__unlock_overdrive_movement,
                                           unlock_mining_overdrive=self.__unlock_overdrive_mining,
                                           unlock_dynamite=self.__unlock_dynamite,
                                           unlock_landmines=self.__unlock_landmines,
                                           unlock_emps=self.__unlock_emps,
                                           unlock_trap_detection=self.__unlock_trap_detection)
        return TechTree(avatar_functions)

    def __increase_movement(self, amt: int) -> None:
        self.movement_speed += amt

    def __increase_drop_rate(self, amt: float) -> None:
        self.drop_rate += amt

    def __unlock_overdrive_movement(self) -> None:
        self.__abilities['Overdrive Movement'] = True

    def __unlock_overdrive_mining(self) -> None:
        self.__abilities['Overdrive Mining'] = True

    def __unlock_dynamite(self) -> None:
        self.__abilities['Dynamite'] = True

    def __unlock_landmines(self) -> None:
        self.__abilities['Landmines'] = True

    def __unlock_emps(self) -> None:
        self.__abilities['EMPs'] = True
        self.__abilities['Landmines'] = False

    def __unlock_trap_detection(self) -> None:
        self.__abilities['Trap Detection'] = True

    # Helper method to create a dictionary that stores bool values for which abilities the player unlocked
    def __create_abilities_dict(self) -> dict:
        abilities = {'Overdrive Movement': False,
                     'Overdrive Mining': False,
                     'Dynamite': False,
                     'Landmines': False,
                     'EMPs': False,
                     'Trap Detection': False}
        return abilities

    def buy_new_tech(self, tech_name: str) -> bool:
        """By giving the name of a tech, this method attempts to buy the tech. It returns a boolean representing if
        the purchase was successful or not."""
        # to prevent players from using this whenever, there can be another check here to see if they are at their base

        tech_info: TechInfo = self.__tech_tree.tech_info(tech_name)

        # If invalid tech_name, throw an error
        if tech_info is None:
            raise ValueError(f'{tech_name} is not a valid tech name.')

        # If the player can't afford the wanted tech, do nothing
        if self.science_points < tech_info.cost:
            return False

        successful: bool = self.__tech_tree.research(tech_name)  # Research the wanted tech

        # Subtract the cost from the player's science_points if successfully researched
        if successful:
            self.science_points -= tech_info.cost

        return successful

    def get_tech_tree(self) -> TechTree:
        return self.__tech_tree

    def is_researched(self, tech_name: str) -> bool:
        """Returns if the given tech was researched."""
        return self.__tech_tree.is_researched(tech_name)

    def get_researched_techs(self) -> list[str]:
        """Returns the list of researched techs."""
        return self.__tech_tree.researched_techs()

    def get_all_tech_names(self) -> list[str]:
        """Returns a list of all possible tech names in a Tech Tree."""
        return self.__tech_tree.tech_names()

    # if avatar calls place dynamite, set to true, i.e. they want to place dynamite
    def placing_dynamite(self) -> bool:
        # This method will be called in the unlock_dynamite method in the else statement for when it's to be used
        self.placing_dynamite = self.dynamite_active_ability.use()  # sets the avatar's bool reference
        return self.placing_dynamite  # return the bool reference to know to place dynamite

    # if avatar calls place trap, set to true, i.e. they want to place trap
    def placing_trap(self) -> bool:
        # This method will be called in the landmine and EMP methods in the else statement for when it's to be used
        self.placing_trap = self.place_trap.use()  # sets the avatar's bool reference
        return self.placing_trap  # return the bool reference to know to place dynamite

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['company'] = self.company
        data['score'] = self.score
        data['science_points'] = self.science_points
        data['position'] = self.position.to_json() if self.position is not None else None
        data['movement_speed'] = self.movement_speed
        data['drop_rate'] = self.drop_rate
        data['tech_tree'] = self.__tech_tree.to_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.company: Company = data['company']
        self.score: int = data['score']
        self.science_points: int = data['science_points']
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.movement_speed = data['movement_speed']
        self.drop_rate = data['drop_rate']
        self.__tech_tree = data['tech_tree']
        return self
