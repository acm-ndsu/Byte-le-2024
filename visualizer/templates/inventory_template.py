import pygame
from matplotlib.animation import Animation

from game.utils.vector import Vector
from visualizer.sprites.inventory.ancient_tech_inventory import AncientTechInventory
from visualizer.sprites.inventory.copium_inventory import CopiumInventory
from visualizer.sprites.inventory.dynamite_ability import DynamiteAbility
from visualizer.sprites.inventory.emp_ability import EmpAbility
from visualizer.sprites.inventory.inventory_backdrop import InventoryBackdrop
from visualizer.sprites.inventory.lambdium_inventory import LambdiumInventory
from visualizer.sprites.inventory.landmine_ability import LandmineAbility
from visualizer.sprites.inventory.science import Science
from visualizer.sprites.inventory.turite_inventory import TuriteInventory
from visualizer.templates.info_template import InfoTemplate
from visualizer.utils.text import Text


class InventoryTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str,
                 company: int) -> None:
        super().__init__(screen, topleft, size, font, color)

        self.backdrop: InventoryBackdrop = InventoryBackdrop(top_left=topleft)
        self.backdrop.add(self.render_list)

        self.company = company
        self.company_text: Text = Text(screen, text=f'{"Church" if company == 1 else "Turing"}',
                                       font_size=48, font_name=self.font, color=self.color,
                                       position=Vector.add_vectors(topleft, Vector(y=25, x=100)))

        self.ancient_tech = AncientTechInventory(top_left=Vector.add_vectors(topleft, Vector(y=100, x=50)))
        self.ancient_tech.add(self.render_list)

        self.ancient_tech_text: Text = Text(screen, text="0", font_size=32, font_name=self.font, color=self.color,
                                            position=Vector.add_vectors(topleft, Vector(y=95, x=100)))

        self.copium = CopiumInventory(top_left=Vector.add_vectors(topleft, Vector(y=150, x=50)))
        self.copium.add(self.render_list)

        self.copium_text = Text(screen, text="0", font_size=32, font_name=self.font, color=self.color,
                                position=Vector.add_vectors(topleft, Vector(y=145, x=100)))

        self.lambdium = LambdiumInventory(top_left=Vector.add_vectors(topleft, Vector(y=200, x=50)))
        self.lambdium.add(self.render_list)

        self.lambdium_text = Text(screen, text="0", font_size=32, font_name=self.font, color=self.color,
                                  position=Vector.add_vectors(topleft, Vector(y=195, x=100)))

        self.turite = TuriteInventory(top_left=Vector.add_vectors(topleft, Vector(y=250, x=50)))
        self.turite.add(self.render_list)

        self.turite_text = Text(screen, text="0", font_size=32, font_name=self.font, color=self.color,
                                position=Vector.add_vectors(topleft, Vector(y=245, x=100)))

        self.dynamite_ability = DynamiteAbility(top_left=Vector.add_vectors(topleft, Vector(y=100, x=225)))
        self.dynamite_ability.add(self.render_list)

        self.emp_ability = EmpAbility(top_left=Vector.add_vectors(topleft, Vector(y=150, x=225)))
        self.emp_ability.add(self.render_list)

        self.landmine_ability = LandmineAbility(top_left=Vector.add_vectors(topleft, Vector(y=200, x=225)))
        self.landmine_ability.add(self.render_list)

        self.science: Science = Science(top_left=Vector.add_vectors(topleft, Vector(y=400, x=50)))

        self.science.add(self.render_list)

        self.science_text: Text = Text(self.screen, text="0", font_size=32, font_name=self.font, color=self.color,
                                       position=Vector.add_vectors(topleft, Vector(y=395, x=100)))

    def recalc_animation(self, turn_log: dict) -> None:
        team_name: str = [client['team_name']
                          for client in turn_log['clients']
                          if client['avatar']['company'] == self.company][0]
        self.company_text.text = f'{"Church" if self.company == 1 else "Turing"}: {team_name}'

        avatar: dict = [client['avatar']
                        for client in turn_log['clients']
                        if client['avatar']['company'] == self.company][0]
        science_points: str = avatar['science_points']

        self.science_text.text = str(science_points)

        inventory: list[dict | None] = [item for item in
                                        turn_log['game_board']
                                        ['inventory_manager']
                                        ['inventories']
                                        [str(self.company)] if item is not None]

        self.ancient_tech_text.text = str(len([item for item in inventory if item.get('object_type', 1) == 15]))
        self.copium_text.text = str(len([item for item in inventory if item.get('object_type', 1) == 13]))
        self.lambdium_text.text = str(len([item for item in inventory if item.get('object_type', 1) == 11]))
        self.turite_text.text = str(len([item for item in inventory if item.get('object_type', 1) == 12]))

        self.dynamite_ability.activated = (avatar['dynamite_active_ability']['is_usable']
                                           and avatar['tech_tree']['Dynamite'])

        self.landmine_ability.activated = (avatar['landmine_active_ability']['is_usable']
                                           and avatar['tech_tree']['Landmines'])

        self.emp_ability.activated = (avatar['emp_active_ability']['is_usable']
                                      and avatar['tech_tree']['EMPs'])

    def render(self) -> None:
        super().render()
        self.company_text.render()
        self.ancient_tech_text.render()
        self.copium_text.render()
        self.lambdium_text.render()
        self.turite_text.render()
        self.science_text.render()
