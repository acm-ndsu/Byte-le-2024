from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self


class Avatar(GameObject):
    def __init__(self, item: Item|None = None, position: tuple[int,int]|None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.held_item: Item|None = item
        self.score: int = 0
        self.position: tuple[int,int]|None = position

    @property
    def held_item(self) -> Item|None:
        return self.__held_item

    @property
    def score(self) -> int:
        return self.__score

    @property
    # return format for tuple (x-position, y-position), assumes (0,0) is top left of the game board, or None
    def position(self) -> tuple[int, int]|None:
        return self.__position

    @held_item.setter
    def held_item(self, item: Item|None) -> None:
        # If it's not an item, and it's not None, raise the error
        if item is not None and not isinstance(item, Item):
            raise ValueError(f"{self.__class__.__name__}.held_item must be an Item or None.")
        self.__held_item = item

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(f"{self.__class__.__name__}.score must be an int.")
        self.__score = score

    @position.setter
    def position(self, position: tuple[int, int]|None) -> None:
        if position is not None and not(isinstance(position, tuple) and list(map(type, position)) == [int, int]):
            raise ValueError(f"{self.__class__.__name__}.position must be a tuple of two ints or None.")
        self.__position = position

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['held_item'] = self.held_item.to_json() if self.held_item is not None else None
        data['score'] = self.score
        data['position'] = self.position
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.score: int = data['score']
        self.position: tuple[int,int]|None = data['position']
        held_item: Item|None = data['held_item']
        if held_item is None:
            self.held_item = None
            return self
        
        match held_item['object_type']:
            case ObjectType.ITEM:
                self.held_item = Item().from_json(data['held_item'])
            case _:
                raise ValueError(f"{self.__class__.__name__}.held_item needs to be an item.")
        
        return self
