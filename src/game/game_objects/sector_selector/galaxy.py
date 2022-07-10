import src.engine as engine

from src.game.game_objects.sector_selector.star import Star

import pygame
import math
import random
import numpy as np


class Galaxy:
    def __init__(self, seed: int = None):
        # Galaxy parameters
        self.number_of_arms = 2
        self.number_of_stars_per_arm = 1000

        self.size = 100
        self._max_angle = math.radians(450)
        self._xy_scale = self.size / self._max_angle

        self.seed = seed
        self._stars = []

        if self.seed is None:
            self.seed = random.randint(0, 1_000_000_000)

        self.surface = pygame.Surface((236, 193))
        self._center = [118, 97]
        self._angle_x = 0
        self._angle_y = math.radians(30)
        self._scale = 1



        self._generate_galaxy()

    def rotate(self, angle_x: float, angle_y: float):
        self._angle_x -= angle_x
        self._angle_y += angle_y

        self._angle_x = self._angle_x % math.tau
        self._angle_y = max(-math.pi / 2, min(math.pi / 2, self._angle_y))

    def move(self, dx: float, dy: float, account_for_zoom: bool = True):
        if account_for_zoom:
            self._center[0] -= dx * self._scale
            self._center[1] -= dy * self._scale

        else:
            self._center[0] -= dx
            self._center[1] -= dy

    def zoom(self, zoom: float, keep_centered: bool = True):
        self._scale *= zoom

        if keep_centered:
            self._center[0] = (self._center[0] - 118) * zoom + 118
            self._center[1] = (self._center[1] - 97) * zoom + 97

    def _generate_galaxy(self):
        self._stars = []
        random.seed(self.seed)

        number_of_arms = 2
        number_of_stars_per_arm = 1000

        limit_angle = self._max_angle / 3
        limit_width = self._max_angle - limit_angle

        max_reduction = 0.8
        plane_sigma = 13
        diff_height_sigma = 5
        min_height_sigma = 1
        height_sigma_power = 2

        for arm in range(number_of_arms):
            offset = arm / number_of_arms * math.tau
            for _ in range(number_of_stars_per_arm):
                angle = random.uniform(0, self._max_angle)
                ratio = angle / self._max_angle

                # Plane deviation
                xy_sigma = plane_sigma
                if angle > limit_angle:
                    multiplier = 1 - ((angle - limit_angle) / limit_width) * max_reduction
                    xy_sigma = plane_sigma * multiplier

                x_deviation = random.gauss(0, xy_sigma)
                y_deviation = random.gauss(0, xy_sigma)

                # Height deviation
                multiplier = ((math.cos(ratio * math.pi)+1) / 2) ** height_sigma_power

                # Star position
                x = angle * math.cos(angle + offset) * self._xy_scale + x_deviation
                y = angle * math.sin(angle + offset) * self._xy_scale + y_deviation
                z = + random.gauss(0, min_height_sigma + diff_height_sigma * multiplier)

                ratio = math.hypot(x, y, z) / self.size
                ratio = min(1.0, max(0.0, ratio + random.gauss(0, 0.5)))
                if ratio < 0.5:
                    if random.uniform(0, 0.5) > ratio:
                        color = 1
                    else:
                        color = 2
                else:
                    if random.uniform(0.5, 1) > ratio:
                        color = 2
                    else:
                        color = 3

                star_pos = x, y, z
                star_surf = engine.resources.images["environment"][f"star_{random.randint(1, 4)}_{color}"]
                star_sprite = engine.scene.Sprite(star_surf, (0, 0))
                self._stars.append(Star(star_pos, star_sprite))

    def _generate_sectors(self):
        test = 10
        nb = 6
        angles = np.geomspace(test + math.radians(25), test + self._max_angle, nb)
        for planet_depth in range(nb):
            angle = self._max_angle - (angles[planet_depth] - test)
            x = angle * math.cos(angle) * self._xy_scale
            y = angle * math.sin(angle) * self._xy_scale
            z = 0

            surf = pygame.Surface((10, 10))
            surf.set_colorkey((0, 0, 0))
            pygame.draw.circle(surf, (255, 0, 0), (4, 4), 5)
            sprite = engine.scene.Sprite(surf, (0, 0))

            self._stars.append(Star((x, y, z), sprite))

    def draw(self) -> pygame.Surface:

        random.seed(50)
        for i in range(100):
            color = random.randint(1, 3)
            posx, posy = random.randint(-5, 236), random.randint(-5, 193)
            self.surface.blit(engine.resources.images["environment"][f"star_{random.randint(1, 4)}_{color}"], (posx, posy))

        cos_x, sin_x = math.cos(self._angle_x), math.sin(self._angle_x)
        cos_y, sin_y = math.cos(self._angle_y), math.sin(self._angle_y)

        for star in self._stars:
            star.draw(self._center, self._scale, cos_x, sin_x, cos_y, sin_y, self.surface)

        return self.surface

    def draw_accessible(self):
        pass
