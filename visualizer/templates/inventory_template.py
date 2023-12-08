import pygame

from game.utils.vector import Vector
from visualizer.sprites.inventory.ancient_tech_inventory import AncientTechInventory
from visualizer.sprites.inventory.copium_inventory import CopiumInventory
from visualizer.sprites.inventory.dynamite_ability import DynamiteAbility
from visualizer.sprites.inventory.emp_ability import EmpAbility
from visualizer.sprites.inventory.lambdium_inventory import LambdiumInventory
from visualizer.sprites.inventory.landmine_ability import LandmineAbility
from visualizer.sprites.inventory.turite_inventory import TuriteInventory
from visualizer.templates.info_template import InfoTemplate


class InventoryTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str, player: int) -> None:
        super().__init__(screen, topleft, size, font, color)
        self.player = player

        self.ancient_tech = AncientTechInventory(top_left=Vector.add_vectors(topleft, Vector(y=100, x=50)))
        self.ancient_tech.add(self.render_list)

        self.copium = CopiumInventory(top_left=Vector.add_vectors(topleft, Vector(y=150, x=50)))
        self.copium.add(self.render_list)

        self.lambdium = LambdiumInventory(top_left=Vector.add_vectors(topleft, Vector(y=200, x=50)))
        self.lambdium.add(self.render_list)

        self.turite = TuriteInventory(top_left=Vector.add_vectors(topleft, Vector(y=250, x=50)))
        self.turite.add(self.render_list)

        self.dynamite_ability = DynamiteAbility(top_left=Vector.add_vectors(topleft, Vector(y=100, x=225)))
        self.dynamite_ability.add(self.render_list)

        self.emp_ability = EmpAbility(top_left=Vector.add_vectors(topleft, Vector(y=150, x=225)))
        self.emp_ability.add(self.render_list)

        self.landmine_ability = LandmineAbility(top_left=Vector.add_vectors(topleft, Vector(y=150, x=225)))
        self.landmine_ability.add(self.render_list)

    def recalc_animation(self, turn_log: dict) -> None:
        ...