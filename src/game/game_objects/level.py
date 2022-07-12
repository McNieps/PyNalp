import src.engine as engine

import pygame
import random


class Level:
    MAX_PLAYER_INDUCED_OFFSET = (40, 30)

    def __init__(self, difficulty: float):
        self.difficulty = difficulty
        self.number_of_events = 5

        # scene
        self.stars = []
        self.number_of_stars = 5000
        self.length = 100_000

        self._generate_level()
        self._generate_scene()

    def _generate_level(self):
        pass

    def _generate_scene(self):
        min_x = int(-self.MAX_PLAYER_INDUCED_OFFSET[0]/2)
        max_x = int(self.MAX_PLAYER_INDUCED_OFFSET[1]/2 + self.length)
        min_y = int(-self.MAX_PLAYER_INDUCED_OFFSET[1]/2)
        max_y = int(self.MAX_PLAYER_INDUCED_OFFSET[1]/2)

        for _ in range(self.number_of_stars):
            star_color = random.randint(1, 3)
            star_type = random.randint(1, 4)
            star_surf = engine.resources.images["environment"][f"star_{star_type}_{star_color}"]

            star_pos = random.randint(min_x, max_x), random.randint(min_y, max_y)
            star_depth = abs(random.gauss(0, 1))
            star_screen_offset = random.randint(-200, 200), random.randint(-150, 150)

            star_sprite = engine.scene.Sprite(star_surf, star_pos, star_depth, star_screen_offset)
            self.stars.append(star_sprite)
