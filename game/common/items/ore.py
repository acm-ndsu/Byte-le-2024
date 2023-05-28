from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from game.common.items.item import Item
from typing import Self


class Ore(Item):
    def __init__(self, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1, position: Vector | None = None, name: str | None = None):
        super.__init__(value,None, durability,quantity,stack_size,position,name)
         

    


   


    
