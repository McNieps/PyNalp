import src.engine as engine

from src.game.game_objects.wave import Wave

import pygame
import random


class Level:
    MAX_PLAYER_INDUCED_OFFSET = (40, 30)

    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        self.number_of_waves = 5

        # level
        self.waves = []

        # scene
        self.stars = []
        self.number_of_stars = 500
        self.length = 100_000

        self._generate_level()
        self._generate_scene()

    def _generate_level(self):
        for i in range(self.number_of_waves):
            wave = Wave(self.difficulty)

            self.waves.append(wave)

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
