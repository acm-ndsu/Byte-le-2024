import pygame

from game.utils.vector import Vector
from visualizer.sprites.scoreboard.number_light import NumberLight
from visualizer.sprites.scoreboard.scoreboard_backdrop import ScoreboardBackdrop
from visualizer.templates.info_template import InfoTemplate


class ScoreboardTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str) -> None:
        super().__init__(screen, topleft, size, font, color)

        self.scoreboard_backdrop: ScoreboardBackdrop = ScoreboardBackdrop(top_left=Vector())
        self.scoreboard_backdrop.add(self.render_list)

        # Team 1 Score
        self.scoreboard_t1_n1: NumberLight = NumberLight(top_left=Vector(x=100, y=6))
        self.scoreboard_t1_n1.add(self.render_list)

        self.scoreboard_t1_n2: NumberLight = NumberLight(top_left=Vector(x=126, y=6))
        self.scoreboard_t1_n2.add(self.render_list)

        self.scoreboard_t1_n3: NumberLight = NumberLight(top_left=Vector(x=152, y=6))
        self.scoreboard_t1_n3.add(self.render_list)

        self.scoreboard_t1_n4: NumberLight = NumberLight(top_left=Vector(x=178, y=6))
        self.scoreboard_t1_n4.add(self.render_list)

        self.scoreboard_t1_n5: NumberLight = NumberLight(top_left=Vector(x=204, y=6))
        self.scoreboard_t1_n5.add(self.render_list)

        self.scoreboard_t1_n6: NumberLight = NumberLight(top_left=Vector(x=230, y=6))
        self.scoreboard_t1_n6.add(self.render_list)

        # Turn numbers
        self.scoreboard_turn_n1: NumberLight = NumberLight(top_left=Vector(x=593, y=6))
        self.scoreboard_turn_n1.add(self.render_list)

        self.scoreboard_turn_n2: NumberLight = NumberLight(top_left=Vector(x=619, y=6))
        self.scoreboard_turn_n2.add(self.render_list)

        self.scoreboard_turn_n3: NumberLight = NumberLight(top_left=Vector(x=645, y=6))
        self.scoreboard_turn_n3.add(self.render_list)

        self.scoreboard_turn_slash: NumberLight = NumberLight(top_left=Vector(x=671, y=6))
        self.scoreboard_turn_slash.character = '/'
        self.scoreboard_turn_slash.add(self.render_list)

        self.scoreboard_turn_t1: NumberLight = NumberLight(top_left=Vector(x=697, y=6))
        self.scoreboard_turn_t1.character = 5
        self.scoreboard_turn_t1.add(self.render_list)

        self.scoreboard_turn_t2: NumberLight = NumberLight(top_left=Vector(x=723, y=6))
        self.scoreboard_turn_t2.character = 0
        self.scoreboard_turn_t2.add(self.render_list)

        self.scoreboard_turn_t3: NumberLight = NumberLight(top_left=Vector(x=749, y=6))
        self.scoreboard_turn_t3.character = 0
        self.scoreboard_turn_t3.add(self.render_list)

        # Team 2 Score
        self.scoreboard_t2_n1: NumberLight = NumberLight(top_left=Vector(x=1110, y=6))
        self.scoreboard_t2_n1.add(self.render_list)

        self.scoreboard_t2_n2: NumberLight = NumberLight(top_left=Vector(x=1136, y=6))
        self.scoreboard_t2_n2.add(self.render_list)

        self.scoreboard_t2_n3: NumberLight = NumberLight(top_left=Vector(x=1162, y=6))
        self.scoreboard_t2_n3.add(self.render_list)

        self.scoreboard_t2_n4: NumberLight = NumberLight(top_left=Vector(x=1188, y=6))
        self.scoreboard_t2_n4.add(self.render_list)

        self.scoreboard_t2_n5: NumberLight = NumberLight(top_left=Vector(x=1214, y=6))
        self.scoreboard_t2_n5.add(self.render_list)

        self.scoreboard_t2_n6: NumberLight = NumberLight(top_left=Vector(x=1240, y=6))
        self.scoreboard_t2_n6.add(self.render_list)


    def recalc_animation(self, turn_log: dict) -> None:
        scores: list[int] = [client['avatar']['score'] if client['avatar'] else 0 for client in turn_log['clients']]
        turn = turn_log['tick']
        self.scoreboard_turn_n1.character, turn = divmod(turn, 100)
        self.scoreboard_turn_n2.character, turn = divmod(turn, 10)
        self.scoreboard_turn_n3.character = turn



        self.scoreboard_t1_n1, scores[0] = divmod(scores[0], 100000)
        self.scoreboard_t1_n2, scores[0] = divmod(scores[0], 10000)
        self.scoreboard_t1_n3, scores[0] = divmod(scores[0], 1000)
        self.scoreboard_t1_n4, scores[0] = divmod(scores[0], 100)
        self.scoreboard_t1_n5, scores[0] = divmod(scores[0], 10)
        self.scoreboard_t1_n6 = scores[0]

        self.scoreboard_t2_n1, scores[1] = divmod(scores[1], 100000)
        self.scoreboard_t2_n2, scores[1] = divmod(scores[1], 10000)
        self.scoreboard_t2_n3, scores[1] = divmod(scores[1], 1000)
        self.scoreboard_t2_n4, scores[1] = divmod(scores[1], 100)
        self.scoreboard_t2_n5, scores[1] = divmod(scores[1], 10)
        self.scoreboard_t2_n6 = scores[1]
