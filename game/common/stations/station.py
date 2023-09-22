from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.quarry_rush.avatar.inventory_manager import InventoryManager
from typing import Self


# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    """
    `Station Class Notes:`

        Station objects inherit from GameObject and can contain Item objects in them.

        Players can interact with Stations in different ways by using the ``take_action()`` method. Whatever is specified
        in this method will control how players interact with the station. The Avatar and Item classes have methods that
        go through this process. Refer to them for more details.

        The Occupiable Station Example class demonstrates an avatar object receiving the station's stored item. The
        Station Receiver Example class demonstrates an avatar depositing its held item into a station. These are simple
        ideas for how stations can be used. These can be heavily added onto for more creative uses!
    """

    def __init__(self, held_item: Item | None = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.STATION
        self.held_item: Item | None = held_item

    # held_item getter and setter methods
    @property
    def held_item(self) -> Item | None:
        return self.__item

    @held_item.setter
    def held_item(self, held_item: Item) -> None:
        if held_item is not None and not isinstance(held_item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None, not {held_item}.')
        self.__item = held_item

    # base of take action method, defined in classes that extend Station (StationExample demonstrates this)
    # InventoryManager added to this method for Byte-le 2024
    def take_action(self, avatar: Avatar, inventory_manager: InventoryManager) -> Item | None:
        pass

    # json methods
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['held_item'] = self.held_item.to_json() if self.held_item is not None else None

        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        held_item: dict = data['held_item']
        if held_item is None:
            self.held_item = None
            return self

        # framework match case for from json, can add more object types that can be item
        match ObjectType(held_item['object_type']):
            case ObjectType.ITEM:
                self.held_item = Item().from_json(held_item)
            case _:
                raise Exception(f'Could not parse held_item: {held_item}')
        return self
