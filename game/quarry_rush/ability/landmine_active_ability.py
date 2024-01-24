from game.quarry_rush.ability.active_ability import ActiveAbility
from game.config import LANDMINE_COOLDOWN
from game.common.enums import ObjectType


class LandmineActiveAbility(ActiveAbility):

    def __init__(self, cooldown: int = LANDMINE_COOLDOWN, fuse: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.LANDMINE_ACTIVE_ABILITY
        self.cooldown: int = cooldown
        self.fuse: int = fuse  # default = 0 to be available right after purchase
