from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self
from game.quarry_rush.active_ability import ActiveAbility


class PlaceTrap(ActiveAbility):

    def __init__(self):
        