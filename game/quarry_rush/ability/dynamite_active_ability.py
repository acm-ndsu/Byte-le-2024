from game.common.enums import ObjectType
from game.quarry_rush.ability.active_ability import ActiveAbility
from typing import Self


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, cooldown: int = 1, fuse: int = 0):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
