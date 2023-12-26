import pygame

from game.utils.vector import Vector
from visualizer.sprites.tech_tree.military.defuse_tech import DefuseTech
from visualizer.sprites.tech_tree.military.dynamite_tech import DynamiteTech
from visualizer.sprites.tech_tree.military.emp_tech import EmpTech
from visualizer.sprites.tech_tree.military.landmine_tech import LandmineTech
from visualizer.sprites.tech_tree.mining.mining1_tech import Mining1Tech
from visualizer.sprites.tech_tree.mining.mining2_tech import Mining2Tech
from visualizer.sprites.tech_tree.mining.mining3_tech import Mining3Tech
from visualizer.sprites.tech_tree.mvts.mvt1_tech import Mvt1Tech
from visualizer.sprites.tech_tree.mvts.mvt2_tech import Mvt2Tech
from visualizer.sprites.tech_tree.mvts.mvt3_tech import Mvt3Tech
from visualizer.templates.info_template import InfoTemplate
from visualizer.sprites.tech_tree.tech_tree_backdrop import TechTreeBackdrop


class TechTreeTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str,
                 company: int) -> None:
        super().__init__(screen, topleft, size, font, color)
        self.company = company

        self.tech_tree_backdrop: TechTreeBackdrop = TechTreeBackdrop(top_left=topleft)
        self.tech_tree_backdrop.add(self.render_list)

        self.mvt1_tech: Mvt1Tech = Mvt1Tech(top_left=Vector.add_vectors(topleft, Vector(x=142, y=33)))
        self.mvt1_tech.add(self.render_list)

        self.mvt2_tech: Mvt2Tech = Mvt2Tech(top_left=Vector.add_vectors(topleft, Vector(x=257, y=33)))
        self.mvt2_tech.add(self.render_list)

        self.mvt3_tech: Mvt3Tech = Mvt3Tech(top_left=Vector.add_vectors(topleft, Vector(x=375, y=33)))
        self.mvt3_tech.add(self.render_list)

        self.mining1_tech: Mining1Tech = Mining1Tech(top_left=Vector.add_vectors(topleft, Vector(x=142, y=97)))
        self.mining1_tech.add(self.render_list)

        self.mining2_tech: Mining2Tech = Mining2Tech(top_left=Vector.add_vectors(topleft, Vector(x=258, y=97)))
        self.mining2_tech.add(self.render_list)

        self.mining3_tech: Mining3Tech = Mining3Tech(top_left=Vector.add_vectors(topleft, Vector(x=375, y=97)))
        self.mining3_tech.add(self.render_list)

        self.dynamite_tech: DynamiteTech = DynamiteTech(top_left=Vector.add_vectors(topleft, Vector(x=142, y=161)))
        self.dynamite_tech.add(self.render_list)

        self.landmine_tech: LandmineTech = LandmineTech(top_left=Vector.add_vectors(topleft, Vector(x=257, y=161)))
        self.landmine_tech.add(self.render_list)

        self.emp_tech: EmpTech = EmpTech(top_left=Vector.add_vectors(topleft, Vector(x=338, y=138)))
        self.emp_tech.add(self.render_list)

        self.defuse_tech: DefuseTech = DefuseTech(top_left=Vector.add_vectors(topleft, Vector(x=389, y=172)))
        self.defuse_tech.add(self.render_list)

    def recalc_animation(self, turn_log: dict) -> None:
        tech_tree: dict = [client['avatar']['tech_tree']
                           for client in turn_log['clients']
                           if client['avatar']['company'] == self.company][0]

        self.mvt1_tech.activated = tech_tree['Improved Drivetrain']
        self.mvt2_tech.activated = tech_tree['Superior Drivetrain']
        self.mvt3_tech.activated = tech_tree['Overdrive Drivetrain']

        self.mining1_tech.activated = tech_tree['Improved Mining']
        self.mining2_tech.activated = tech_tree['Superior Mining']
        self.mining3_tech.activated = tech_tree['Overdrive Mining']

        self.dynamite_tech.activated = tech_tree['Dynamite']
        self.landmine_tech.activated = tech_tree['Landmines']
        self.emp_tech.activated = tech_tree['EMPs']
        self.defuse_tech.activated = tech_tree['Trap Defusal']
