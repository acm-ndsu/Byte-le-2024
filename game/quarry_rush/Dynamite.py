from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.quarry_rush.active_ability import ActiveAbility


class Dynamite(ActiveAbility):

    def __init__(self):
        super().__init__()

    def blast_radius(self, blast_radius, ):
