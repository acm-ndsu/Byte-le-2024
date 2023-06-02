from typing import Self

from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.quarry_rush.tech import TechInfo
from game.utils.vector import Vector
from game.quarry_rush.tech_tree import TechTree
from game.quarry_rush.player_functions import PlayerFunctions
from typing import Callable


class LockedTechError(Exception):
    "Raised when trying to access a tech out of order."
    pass


class Avatar(GameObject):
    """
    Notes for the inventory:

    The avatar's inventory is a list of items. Each item has a quantity and a stack_size (the max amount of an
    item that can be held in a stack. Think of the Minecraft inventory).

    This upcoming example is just to facilitate understanding the concept. The Dispensing Station concept that will
    be mentioned is completely optional to implement if you desire. The Dispensing Station is used to help with the
    explanation.

    ----

    Items:
        Every Item has a quantity and a stack_size. The quantity is how much of the Item the player *currently* has.
        The stack_size is the max of that Item that can be in a stack. For example, if the quantity is 5, and the
        stack_size is 5 (5/5), the item cannot be added to that stack

    Picking up items:
    Example 1:
        When you pick up an item (which will now be referred to as picked_up_item), picked_up_item has a given
        quantity. In this case, let's say the quantity of picked_up_item is 2.

        Imagine you already have this item in your inventory (which will now be referred to as inventory_item),
        and inventory_item has a quantity of 1 and a stack_size of 10 (think of this as a fraction: 1/10).

        When you pick up picked_up_item, inventory_item will be checked.
        If picked_up_item's quantity + inventory_item < stack_size, it'll be added without issue.
        Remember, for this example: picked_up_item quantity is 2, and inventory_item quantity is 1, and stack_size
        is 10.
            Inventory_item quantity before picking up: 1/10
                2 + 1 < 10 --> True
            Inventory_item quantity after picking up: 3/10

    ----

    Example 2:
        For the next two examples, the total inventory size will be considered.

        Let's say inventory_item has quantity 4 and a stack_size of 5. Now say that picked_up_item has quantity 3.
        Recall: if picked_up_item's quantity + inventory_item < stack_size, it will be added without issue
            Inventory_item quantity before picking up: 4/5
                3 + 4 < 5 --> False

        What do we do in this situation? If you want to add picked_up_item to inventory_item and there is an
        overflow of quantity, that is handled for you.

        Let's say that your inventory size (which will now be referred to as max_inventory_size) is 5. You already
        have inventory_item in there that has a quantity of 4 and a stack_size of 5. An image of the inventory is
        below. 'None' is used to help show the max_inventory_size. Inventory_item quantity and stack_size will be
        listed in parentheses as a fraction.
            Inventory:
            [inventory_item (4/5), None, None, None, None]

        Now we will add picked_up_item and its quantity of 3:
            Inventory before:
            [inventory_item (4/5), None, None, None, None]

            3 + 4 < 5 --> False
                inventory_item (4/5) will now be inventory_item (5/5)
                picked_up_item now has a quantity of 2
                Since we have a surplus, we will append the same item with a quantity of 2 in the inventory.

            The result is:
            [inventory_item (5/5), inventory_item (2/5), None, None, None]

    ----
    Example 3:

        For this last example, assume your inventory looks like this:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (4/5)]

        You can only fit one more inventory_item into the last stack before the inventory is full.
        Let's say that picked_up_item has quantity of 3 again.

        Inventory before:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (4/5)]
            3 + 4 < 5 --> False
            inventory_item (4/5) will now be inventory_item (5/5)
            picked_up_item now has a quantity of 2
            However, despite the surplus, we cannot add it into our inventory, so the remaining quantity of
            picked_up_item is left where it was first found.
        Inventory after:
        [inventory_item (5/5), inventory_item (5/5) inventory_item (5/5) inventory_item (5/5), inventory_item (5/5)]
    """

    def __init__(self, position: Vector | None = None, max_inventory_size: int = 50):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.score: int = 0
        self.science_points: int = 0
        self.position: Vector | None = position
        self.max_inventory_size: int = max_inventory_size
        self.inventory: list[Item | None] = [None] * max_inventory_size
        self.held_item: Item | None = self.inventory[0]
        self.__held_index: int = 0
        self.movement_speed: int = 1  # determines how many tiles the player moves
        self.drop_rate: float = 1.0  # determines how many items are dropped after mining
        self.__abilities: dict = self.__create_abilities_dict()  # used to manage unlocking new abilities
        self.__tech_tree: TechTree = self.__create_tech_tree()  # the tech tree cannot be set; made private for security

    @property
    def held_item(self) -> Item | None:
        self.__clean_inventory()
        return self.inventory[self.__held_index]

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
    def inventory(self) -> list[Item | None]:
        return self.__inventory

    @property
    def max_inventory_size(self) -> int:
        return self.__max_inventory_size

    @property
    def movement_speed(self):
        return self.__movement_speed

    @property
    def drop_rate(self):
        return self.__drop_rate

    @held_item.setter
    def held_item(self, item: Item | None) -> None:
        self.__clean_inventory()

        # If it's not an item, and it's not None, raise the error
        if item is not None and not isinstance(item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None.')

        # If the item is not contained in the inventory, the error will be raised.
        if not self.inventory.__contains__(item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be set to an item that already exists'
                             f' in the inventory.')

        # If the item is contained in the inventory, set the held_index to that item's index
        self.__held_index = self.inventory.index(item)

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

    @inventory.setter
    def inventory(self, inventory: list[Item | None]) -> None:
        # If every item in the inventory is not of type None or Item, throw an error
        if inventory is None or not isinstance(inventory, list) \
                or (len(inventory) > 0 and any(map(lambda item: item is not None and not isinstance(item, Item),
                                                   inventory))):
            raise ValueError(f'{self.__class__.__name__}.inventory must be a list of Items.')
        if len(inventory) > self.max_inventory_size:
            raise ValueError(f'{self.__class__.__name__}.inventory size must be less than or equal to '
                             f'max_inventory_size')
        self.__inventory: list[Item] = inventory

    @max_inventory_size.setter
    def max_inventory_size(self, size: int) -> None:
        if size is None or not isinstance(size, int):
            raise ValueError(f'{self.__class__.__name__}.max_inventory_size must be an int.')

        if size < 0:
            raise ValueError(f'{self.__class__.__name__}.max_inventory_size must be a positive int.')

        self.__max_inventory_size: int = size

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
        player_functions = PlayerFunctions(increase_movement=lambda x: self.movement_speed + x,
                                           increase_mining=lambda x: self.drop_rate + x,
                                           unlock_movement_overdrive=self.__unlock_overdrive_movement,
                                           unlock_mining_overdrive=self.__unlock_overdrive_mining,
                                           unlock_dynamite=self.__unlock_dynamite,
                                           unlock_landmines=self.__unlock_landmines,
                                           unlock_emps=self.__unlock_emps,
                                           unlock_trap_detection=self.__unlock_trap_detection)
        return TechTree(player_functions)

    def __unlock_overdrive_movement(self) -> None:
        # If the player hasn't unlocked Unnamed Drivetrain Tech, raise an error
        if not self.__tech_tree.is_researched('Unnamed Drivetrain Tech'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock Unnamed Drivetrain Tech before using '
                                  f'Overdrive Movement.')

        # If the player hasn't unlocked Overdrive Movement, set the abilities value to true and research it
        if not self.__abilities['Overdrive Movement']:
            self.__abilities['Overdrive Movement'] = True
            self.__tech_tree.research('Overdrive Movement')
        # otherwise, use the Overdrive Movement ability
        else:
            pass  # will be implemented later as development progresses

    def __unlock_overdrive_mining(self) -> None:
        # If the player hasn't unlocked Unnamed Mining Tech, raise an error
        if not self.__tech_tree.is_researched('Unnamed Mining Tech'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock Unnamed Mining Tech before using '
                                  f'Overdrive Mining.')

        # If the player hasn't unlocked Overdrive Mining, set the abilities value to true and research it
        if not self.__abilities['Overdrive Mining']:
            self.__abilities['Overdrive Mining'] = True
            self.__tech_tree.research('Overdrive Mining')
        # otherwise, use the Overdrive Mining ability
        else:
            pass  # will be implemented later as development progresses

    def __unlock_dynamite(self) -> None:
        # If the player hasn't unlocked High Yield Drilling, raise an error
        if not self.__tech_tree.is_researched('High Yield Drilling'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock High Yield Drilling before using '
                                  f'Dynamite.')

        # If the player hasn't unlocked Dynamite, set the abilities value to true and research it
        if not self.__abilities['Dynamite']:
            self.__abilities['Dynamite'] = True
            self.__tech_tree.research('Dynamite')
        # otherwise, use the Dynamite ability
        else:
            pass  # will be implemented later as development progresses

    def __unlock_landmines(self) -> None:
        # If the player hasn't unlocked Dynamite, raise an error
        if not self.__tech_tree.is_researched('Dynamite'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock Dynamite before using '
                                  f'Landmines.')

        # If the player hasn't unlocked Landmines, set the abilities value to true and research it
        if not self.__abilities['Landmines']:
            self.__abilities['Landmines'] = True
            self.__tech_tree.research('Landmines')
        # otherwise, use the Landmine ability
        else:
            pass  # will be implemented later as development progresses

    def __unlock_emps(self) -> None:
        # If the player hasn't unlocked Landmines, raise an error
        if not self.__tech_tree.is_researched('Landmines'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock Landmines before using '
                                  f'EMPs.')

        # If the player hasn't unlocked EMPs or Trap Detection, set the abilities value to true and research it
        if not self.__abilities['EMPs'] and not self.__abilities['Trap Detection']:
            self.__abilities['EMPs'] = True
            self.__abilities['Landmines'] = False  # Landmines will be locked again since player upgraded from them
            self.__tech_tree.research('EMPs')
        # otherwise, use the EMP ability
        else:
            pass  # will be implemented later as development progresses

    def __unlock_trap_detection(self) -> None:
        # If the player hasn't unlocked Landmines, raise an error
        if not self.__tech_tree.is_researched('Landmines'):
            raise LockedTechError(f'{self.__class__.__name__} must unlock Landmines before using '
                                  f'Trap Detection.')

        # If the player hasn't unlocked Trap Detection or EMPs, set the abilities value to true and research it
        if not self.__abilities['Trap Detection'] and not self.__abilities['EMPs']:
            self.__abilities['Trap Detection'] = True
            self.__tech_tree.research('Trap Detection')
        # otherwise, use the Trap Detection ability
        else:
            pass  # will be implemented later as development progresses

    # Helper method to create a dictionary that stores bool values for which abilities the player unlocked
    def __create_abilities_dict(self) -> dict:
        abilities = {'Overdrive Movement': False,
                     'Overdrive Mining': False,
                     'Dynamite': False,
                     'Landmines': False,
                     'EMPs': False,
                     'Trap Detection': False}
        return abilities

    def buy_new_tech(self, tech_name: str) -> None:
        # to prevent players from using this whenever, there can be another check here to see if they are at their base

        tech_info: TechInfo = self.__tech_tree.tech_info(tech_name)

        # If invalid tech_name, throw an error
        if tech_info is None:
            raise ValueError(f'{tech_name} is not a valid tech name.')
        
        # If the player can't afford the wanted tech, do nothing
        if self.science_points < tech_info.cost:
            return

        self.__tech_tree.research(tech_name)  # Research the wanted tech
        self.science_points -= tech_info.cost  # Subtract the cost from the player's science_points

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

    # Ignore these for now. These were for another purpose, but will be commented out for now.

    # def get_tech_tree(self) -> dict[str, bool]:
    #     """Returns a dictionary of tech names and booleans representing the entire tech tree and which techs
    #     have been researched."""
    #     tree_dict = dict(zip(self.__tech_tree.tech_names(), self.__is_researched_whole_tree()))
    #     return tree_dict
    #
    # def __is_researched_whole_tree(self) -> list[bool]:
    #     """Private method that returns a list of boolean representing what techs the player has researched from
    #     the entire tech tree."""
    #     values: list[bool] = []
    #     for tech in self.__tech_tree.tech_names():
    #         values.append(self.is_researched(tech))
    #     return values

    # End Tech Tree methods and implementation--------------------------------------------------------------------------

    # Private helper method that cleans the inventory of items that have a quantity of 0. This is a safety check
    def __clean_inventory(self) -> None:
        """
        This method is used to manage the inventory. Whenever an item has a quantity of 0, it will set that item object
            to None since it doesn't exist in the inventory anymore. Otherwise, if there are multiple instances of an
            item in the inventory, and they can be consolidated, this method does that.

        Example: In inventory[0], there is a stack of gold with a quantity and stack_size of 5. In inventory[1], there
            is another stack of gold with quantity of 3, stack size of 5. If you want to take away 4 gold, inventory[0]
            will have quantity 1, and inventory[1] will have quantity 3. Then, when clean_inventory is called, it will
            consolidate the two. This mean that inventory[0] will have quantity 4 and inventory[1] will be set to None.
        :return: None
        """

        # This condenses the inventory if there are duplicate items and combines them together
        for i, item in enumerate(self.inventory):
            [j.pick_up(item) for j in self.inventory[:i] if j is not None]

        # This removes any items in the inventory that have a quantity of 0 and replaces them with None
        remove: list[int] = [x[0] for x in enumerate(self.inventory) if x[1] is not None and x[1].quantity == 0]
        for i in remove:
            self.inventory[i] = None

    def drop_held_item(self) -> Item | None:
        """
        Call this method when a station is taking the held item from the avatar.

        ----

        This method can be modified more for different scenarios where the held item would be dropped
            (e.g., you make a game where being attacked forces you to drop your held item).

        ----

        If you want the held item to go somewhere specifically and not become None, that can be changed too.

        ----

        Make sure to keep clean inventory in this method.
        """
        # The held item will be taken from the avatar will be replaced with None in the inventory
        held_item = self.held_item
        self.inventory[self.__held_index] = None

        self.__clean_inventory()

        return held_item

    def take(self, item: Item | None) -> Item | None:
        """
        To use this method, pass in an item object. Whatever this item's quantity is will be the amount subtracted from
            the avatar's inventory. For example, if the item in the inventory is has a quantity of 5 and this method is
            called with the parameter having a quantity of 2, the item in the inventory will have a quantity of 3.

        ----

        Furthermore, when this method is called and the potential item is taken away, the clean_inventory method is
            called. It will consolidate all similar items together to ensure that the inventory is clean.

        ----

        Reference test_avatar_inventory.py and the clean_inventory method for further documentation on this method and
            how the inventory is managed.

        ----

        :param item:
        :return: Item or None
        """
        # Calls the take method on every index on the inventory. If i isn't None, call the method
        # NOTE: If the list is full of None (i.e., no Item objects are in it), nothing will happen
        [item := i.take(item) for i in self.inventory if i is not None]
        self.__clean_inventory()
        return item

    def pick_up(self, item: Item | None) -> Item | None:
        self.__clean_inventory()

        # Calls the pick_up method on every index on the inventory. If i isn't None, call the method
        [item := i.pick_up(item) for i in self.inventory if i is not None]

        # If the inventory has a slot with None, it will replace that None value with the item
        if self.inventory.__contains__(None):
            index = self.inventory.index(None)
            self.inventory.pop(index)
            self.inventory.insert(index, item)
            # Nothing is then returned
            return None

        # If the item can't be in the inventory, return it
        return item

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['held_index'] = self.__held_index
        data['score'] = self.score
        data['science_points'] = self.science_points
        data['position'] = self.position.to_json() if self.position is not None else None
        data['inventory'] = self.inventory
        data['max_inventory_size'] = self.max_inventory_size
        data['movement_speed'] = self.movement_speed
        data['drop_rate'] = self.drop_rate
        data['tech_tree'] = self.__tech_tree.to_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__held_index = data['held_index']
        self.score: int = data['score']
        self.science_points: int = data['science_points']
        self.position: Vector | None = None if data['position'] is None else Vector().from_json(data['position'])
        self.inventory: list[Item] = data['inventory']
        self.max_inventory_size: int = data['max_inventory_size']
        self.held_item: Item | None = self.inventory[data['held_index']]
        self.movement_speed = data['movement_speed']
        self.drop_rate = data['drop_rate']
        self.__tech_tree = data['tech_tree']
        return self
