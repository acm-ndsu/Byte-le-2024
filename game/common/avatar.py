from typing import Self

from game.common.enums import ObjectType, Company
from game.common.game_object import GameObject
from game.quarry_rush.ability.emp_active_ability import EMPActiveAbility
from game.quarry_rush.ability.landmine_active_ability import LandmineActiveAbility
from game.quarry_rush.tech.tech import TechInfo
from game.utils.vector import Vector
from game.quarry_rush.tech.tech_tree import TechTree
from game.quarry_rush.avatar.avatar_functions import AvatarFunctions
from game.quarry_rush.ability.dynamite_active_ability import DynamiteActiveAbility


class Avatar(GameObject):
    """
    `Avatar Inventory Notes:`

        The avatar's inventory is a list of items. Each item has a quantity and a stack_size (the max amount of an
        item that can be held in a stack. Think of the Minecraft inventory).

        This upcoming example is just to facilitate understanding the concept. The Dispensing Station concept that will
        be mentioned is completely optional to implement if you desire. The Dispensing Station is used to help with the
        explanation.

        ----

        **Items:**
            Every Item has a quantity and a stack_size. The quantity is how much of the Item the player *currently* has.
            The stack_size is the max of that Item that can be in a stack. For example, if the quantity is 5, and the
            stack_size is 5 (5/5), the item cannot be added to that stack

        -----

        **Picking up items:**

            Example 1:
                When you pick up an item (which will now be referred to as picked_up_item), picked_up_item has a given
                quantity. In this case, let's say the quantity of picked_up_item is 2.

                Imagine you already have this item in your inventory (which will now be referred to as inventory_item),
                and inventory_item has a quantity of 1 and a stack_size of 10 (think of this as a fraction: 1/10).

                When you pick up picked_up_item, inventory_item will be checked.
                If picked_up_item's quantity + inventory_item < stack_size, it'll be added without issue.
                Remember, for this example: picked_up_item quantity is 2, and inventory_item quantity is 1, and
                stack_size is 10.

                    Inventory_item quantity before picking up: 1/10
                    ::
                        2 + 1 < 10 --> True
                    Inventory_item quantity after picking up: 3/10

            ----

            Example 2:
                For the next two examples, the total inventory size will be considered.

                Let's say inventory_item has quantity 4 and a stack_size of 5. Now say that picked_up_item has
                quantity 3.

                Recall: if picked_up_item's quantity + inventory_item < stack_size, it will be added without issue

                    Inventory_item quantity before picking up: 4/5
                    ::
                        3 + 4 < 5 --> False

                What do we do in this situation? If you want to add picked_up_item to inventory_item and there is an
                overflow of quantity, that is handled for you.

                Let's say that your inventory size (which will now be referred to as max_inventory_size) is 5. You
                already have inventory_item in there that has a quantity of 4 and a stack_size of 5. An image of the
                inventory is below. 'None' is used to help show the max_inventory_size. Inventory_item quantity and
                stack_size will be listed in parentheses as a fraction.
                ::
                    Inventory:
                    [
                        inventory_item (4/5),
                        None,
                        None,
                        None,
                        None
                    ]

                Now we will add picked_up_item and its quantity of 3:
                ::
                    Inventory before:
                    [
                        inventory_item (4/5),
                        None,
                        None,
                        None,
                        None
                    ]

                    3 + 4 < 5 --> False

                inventory_item (4/5) will now be inventory_item (5/5)
                picked_up_item now has a quantity of 2 instead of 3
                Since we have a surplus, we will append the same item with a quantity of 2 in the inventory.
                ::
                    The result is:
                    [
                        inventory_item (5/5),
                        inventory_item (2/5),
                        None,
                        None,
                        None
                    ]

            ----

            Example 3:

                You can only fit one more inventory_item into the last stack before the inventory is full.
                Let's say that picked_up_item has quantity of 3 again.
                ::
                    Inventory before:
                    [
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (4/5)
                    ]

                        3 + 4 < 5 --> False

                inventory_item (4/5) will now be inventory_item (5/5)
                picked_up_item now has a quantity of 2
                However, despite the surplus, we cannot add it into our inventory, so the remaining quantity of
                picked_up_item is left where it was first found.
                ::
                    Inventory after:
                    [
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (5/5),
                        inventory_item (5/5)
                    ]
    """

    def __init__(self, company: Company = Company.CHURCH, position: Vector | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.score: int = 0
        self.science_points: int = 0
        self.position: Vector | None = position
        self.movement_speed: int = 1  # determines how many tiles the player moves
        self.drop_rate: int = 1  # determines how many items are dropped after mining
        self.abilities: dict = self.__create_abilities_dict()  # used to manage unlocking new abilities
        self.__tech_tree: TechTree = self.__create_tech_tree()  # the tech tree cannot be set; made private for security
        self.__company: Company = company
        self.dynamite_active_ability: DynamiteActiveAbility = DynamiteActiveAbility()
        self.landmine_active_ability: LandmineActiveAbility = LandmineActiveAbility()
        self.emp_active_ability: EMPActiveAbility = EMPActiveAbility()

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

    @property
    def abilities(self):
        return self.__abilities

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
    def drop_rate(self, drop_rate: int) -> None:
        if drop_rate is None or not isinstance(drop_rate, int):
            raise ValueError(f'{self.__class__.__name__}.drop_rate must be an int.')

        if drop_rate < 0:
            raise ValueError(f'{self.__class__.__name__}.drop_rate must be a positive int.')

        self.__drop_rate = drop_rate

    @abilities.setter
    def abilities(self, abilities: dict[bool]) -> None:
        if abilities is None or not isinstance(abilities, dict):
            raise ValueError(f'{self.__class__.__name__}.abilities must be a dict.')

        for ability, value in abilities.items():
            if value is None or not isinstance(value, bool):
                raise ValueError(f'Every value in the {self.__class__.__name__}.abilities dict must be a bool.')

        self.__abilities = abilities

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
                                           unlock_trap_defusal=self.__unlock_trap_defusal)
        return TechTree(avatar_functions)

    def __increase_movement(self, amt: int) -> None:
        self.movement_speed += amt
        match self.movement_speed:
            case 2:
                self.abilities['Improved Drivetrain'] = True
            case 3:
                self.abilities['Superior Drivetrain'] = True
            case _:
                self.abilities['Overdrive Drivetrain'] = True

    def __increase_drop_rate(self, amt: int) -> None:
        self.drop_rate += amt
        match self.drop_rate:
            case 2:
                self.abilities['Improved Mining'] = True
            case 3:
                self.abilities['Superior Mining'] = True
            case _:
                self.abilities['Overdrive Mining'] = True

    def __unlock_overdrive_movement(self) -> None:
        self.abilities['Overdrive Drivetrain'] = True

    def __unlock_overdrive_mining(self) -> None:
        self.abilities['Overdrive Mining'] = True

    def __unlock_dynamite(self) -> None:
        self.abilities['Dynamite'] = True

    def __unlock_landmines(self) -> None:
        self.abilities['Landmines'] = True

    def __unlock_emps(self) -> None:
        self.abilities['EMPs'] = True
        self.abilities['Landmines'] = False

    def __unlock_trap_defusal(self) -> None:
        self.abilities['Trap Defusal'] = True

    # Helper method to create a dictionary that stores bool values for which abilities the player unlocked
    def __create_abilities_dict(self) -> dict:
        abilities = {'Improved Drivetrain': False,
                     'Superior Drivetrain': False,
                     'Overdrive Drivetrain': False,
                     'Improved Mining': False,
                     'Superior Mining': False,
                     'Overdrive Mining': False,
                     'Dynamite': False,
                     'Landmines': False,
                     'EMPs': False,
                     'Trap Defusal': False}
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
            self.score += tech_info.point_value

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

    # Dynamite placing functionality ----------------------------------------------------------------------------------
    # if avatar calls place dynamite, set to true, i.e. they want to place dynamite
    def can_place_dynamite(self) -> bool:
        return self.abilities['Dynamite'] and self.dynamite_active_ability.is_usable

    def can_place_landmine(self) -> bool:
        return self.abilities['Landmines'] and self.landmine_active_ability.is_usable

    def can_place_emp(self) -> bool:
        return self.abilities['EMPs'] and self.emp_active_ability.is_usable and not self.abilities['Landmines']

    def can_defuse_trap(self) -> bool:
        return self.abilities['Trap Defusal']

    # method to return the opposing team based on the avatar's company
    def get_opposing_team(self) -> Company:
        return Company.CHURCH if self.company is Company.TURING else Company.TURING

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['company'] = self.company.value
        data['score'] = self.score
        data['science_points'] = self.science_points
        data['position'] = self.position.to_json() if self.position is not None else None
        data['movement_speed'] = self.movement_speed
        data['drop_rate'] = self.drop_rate
        data['tech_tree'] = self.abilities
        data['dynamite_active_ability'] = self.dynamite_active_ability.to_json()
        data['landmine_active_ability'] = self.landmine_active_ability.to_json()
        data['emp_active_ability'] = self.emp_active_ability.to_json()
        # data['tech_tree'] = self.__tech_tree.to_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.company: Company = Company(data['company'])
        self.score: int = data['score']
        self.science_points: int = data['science_points']
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.movement_speed = data['movement_speed']
        self.drop_rate = data['drop_rate']
        self.abilities = data['tech_tree']
        self.__tech_tree = data['tech_tree']
        self.dynamite_active_ability = DynamiteActiveAbility().from_json(data['dynamite_active_ability'])
        self.landmine_active_ability = LandmineActiveAbility().from_json(data['landmine_active_ability'])
        self.emp_active_ability = EMPActiveAbility().from_json(data['emp_active_ability'])
        return self
