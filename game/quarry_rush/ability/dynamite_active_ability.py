from game.common.enums import ObjectType
from game.quarry_rush.ability.active_ability import ActiveAbility
from game.config import DYNAMITE_COOLDOWN
from typing import Self


class DynamiteActiveAbility(ActiveAbility):

    def __init__(self, cooldown: int = DYNAMITE_COOLDOWN, fuse: int = 0):
        super().__init__()
        self.object_type = ObjectType.DYNAMITE_ACTIVE_ABILITY
        self.cooldown = cooldown
        self.fuse = fuse  # default = 0 to be available right after purchase
