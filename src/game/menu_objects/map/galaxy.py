import src.engine as engine

from src.game.menu_objects.map.star import Star
from src.game.menu_objects.map.sector import Sector

import pygame
import math
import random
import numpy as np


class Galaxy:
    def __init__(self, seed: int = None):
        self.seed = seed
        if self.seed is None:
            self.seed = random.randint(0, 1_000_000_000)

        # Galaxy attributes
        self._number_of_arms = 2
        self._number_of_stars_per_arm = 1000
        self._size = 100
        self._max_angle = math.radians(450)
        self._xy_scale = self._size / self._max_angle
        self._stars = []

        # Sector attributes
        self.sectors: list[Sector] = []
        self._sectors_choices = [1, 2, 3, 3, 2, 1]
        self._space_between_sector = 20
        self._available_sectors: list[Sector] = self.sectors
        self.selected_sector = None
        self.hovered_sector = None
        self.current_sector = None

        self._leading_graph = {0: (1, 2),   # I know there are better ways to do this.
                               1: (3, 4),
                               2: (4, 5),
                               3: (6, 7),
                               4: (6, 7, 8),
                               5: (7, 8),
                               6: (9,),
                               7: (9, 10),
                               8: (10,),
                               9: (11,),
                               10: (11,),
                               11: ()}

        # Display attributes
        self.surface = pygame.Surface((236, 193))
        self._rect = pygame.Rect(17, 40, 236, 193)
        self._center = [118, 97]
        self._angle_x = 0
        self._angle_y = math.radians(30)
        self._scale = 1
        self._select_state = 0
        self._bg_stars = []

        # GUI
        self.selection_sprites = [engine.scene.Sprite(engine.resources.images["sector_selection"][f"selected_{i}"],
                                                      (0, 0)) for i in range(1, 5)]
        self.position_sprite = engine.scene.Sprite(engine.resources.images["sector_selection"]["pointer"], (0, 0))

        # Generate
        self._generate_background()
        self._generate_galaxy()
        self._generate_sectors()

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
            self._center[0] = int((self._center[0] - 118) * zoom + 118)
            self._center[1] = int((self._center[1] - 97) * zoom + 97)

    def click(self, mouse_pos: tuple[int, int]):
        if not self._rect.collidepoint(*mouse_pos):
            return

        relative_pos = mouse_pos[0] - self._rect.left, mouse_pos[1] - self._rect.top

        for sector in self.current_sector.lead_to:
            if sector.rect.collidepoint(*relative_pos):

                if sector is self.selected_sector:
                    self.selected_sector = None
                else:
                    self.selected_sector = sector
                    engine.resources.play_sound(["click"])

    def hover(self, mouse_pos: tuple[int, int]):
        if not self._rect.collidepoint(*mouse_pos):
            self.hovered_sector = None
            return

        relative_pos = mouse_pos[0] - self._rect.left, mouse_pos[1] - self._rect.top

        sector_to_inform = None
        for sector in self.sectors:
            if sector not in [self.current_sector, self.selected_sector] and sector.rect.collidepoint(*relative_pos):
                sector_to_inform = sector

        if not sector_to_inform:
            self.hovered_sector = None
            return

        if sector_to_inform is not self.hovered_sector:
            engine.resources.play_sound(("click",))

        for dest_sector in sector_to_inform.lead_to:
            self._draw_line_between_sector(sector_to_inform, dest_sector, (141, 105, 122), width=4)
            self._draw_line_between_sector(sector_to_inform, dest_sector, (255, 236, 214), width=2)
        self.hovered_sector = sector_to_inform

    def reset(self):
        self._center = [118, 97]
        self._angle_x = 0
        self._angle_y = math.radians(30)
        self._scale = 1

    def _generate_background(self):
        for i in range(100):
            _type = random.randint(1, 4)
            _color = random.randint(1, 3)
            star_surf = engine.resources.images["environment"][f"star_{_type}_{_color}"]
            star_pos = random.randint(-5, 236), random.randint(-5, 193)
            self._bg_stars.append(engine.scene.Sprite(star_surf, star_pos))

    def _generate_galaxy(self):
        self._stars = []
        random.seed(self.seed)

        limit_angle = self._max_angle / 3
        limit_width = self._max_angle - limit_angle

        max_reduction = 0.8
        plane_sigma = 13
        diff_height_sigma = 5
        min_height_sigma = 1
        height_sigma_power = 2

        for arm in range(self._number_of_arms):
            offset = arm / self._number_of_arms * math.tau
            for _ in range(self._number_of_stars_per_arm):
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

                ratio = math.hypot(x, y, z) / self._size
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

        angles = np.geomspace(10 + math.radians(25), 10 + self._max_angle, len(self._sectors_choices))
        num = -1
        for sector_depth in range(len(self._sectors_choices)):
            for num_in_depth in range(self._sectors_choices[sector_depth]):
                num += 1

                # Sector position
                angle = self._max_angle - (angles[sector_depth] - 10)
                x = angle * math.cos(angle) * self._xy_scale  # + random.gauss(0, 8)
                y = angle * math.sin(angle) * self._xy_scale  # + random.gauss(0, 8)
                z = random.gauss(0, 3)

                # Offsetting sector
                if self._sectors_choices[sector_depth] > 1:
                    tot_dist = (self._sectors_choices[sector_depth] - 1) * self._space_between_sector
                    offset = -tot_dist / 2
                    dist = tot_dist / (self._sectors_choices[sector_depth] - 1)
                    curr = offset + num_in_depth * dist

                    angle += random.gauss(0, math.radians(10))

                    x += math.cos(angle) * curr + random.gauss(0, 2)
                    y += math.sin(angle) * curr + random.gauss(0, 2)

                # Sector style
                _format = random.randint(5, 6)
                _color = random.randint(1, 2)
                surf = engine.resources.images["environment"][f"star_{_format}_{_color}"]
                sprite = engine.scene.Sprite(surf, (0, 0))

                # Creating objects
                star = Star((x, y, z), sprite)
                sector = Sector(num, sector_depth, star)

                self.sectors.append(sector)

        # Connecting sectors togethers
        for i in self._leading_graph:
            for dest_index in self._leading_graph[i]:
                self.sectors[i].add_destination(self.sectors[dest_index])

        # Adding super secret sector
        chti_sprite = engine.scene.Sprite(engine.resources.images["sector_selection"]["holy_chti"], (0, 0))
        chti_star = Star((10000, 10000, 5000), chti_sprite)
        chti_sector = Sector(666, 666, chti_star)
        self.sectors.append(chti_sector)

        self.current_sector = self.sectors[0]

    def _draw_line_between_sector(self,
                                  sector_1: Sector,
                                  sector_2: Sector,
                                  color: tuple[int, int, int],
                                  width: int = 2,
                                  offset: tuple[int, int] = (0, 0)):

        start_pos = tuple([int(sector_1.position[i] + offset[i]) for i in range(2)])
        end_pos = tuple([int(sector_2.position[i] + offset[i]) for i in range(2)])

        pygame.draw.line(self.surface, color, start_pos, end_pos, width)

    def draw_background(self):
        self.surface.fill((13, 43, 69))
        for bg_star in self._bg_stars:
            bg_star.raw_draw(self.surface, False)

    def draw_galaxy(self):
        cos_x, sin_x = math.cos(self._angle_x), math.sin(self._angle_x)
        cos_y, sin_y = math.cos(self._angle_y), math.sin(self._angle_y)

        for star in self._stars:
            star.draw(self._center, self._scale, cos_x, sin_x, cos_y, sin_y, self.surface)

    # TODO rework this
    def draw_accessible(self):
        cos_x, sin_x = math.cos(self._angle_x), math.sin(self._angle_x)
        cos_y, sin_y = math.cos(self._angle_y), math.sin(self._angle_y)

        for sector in self.sectors:
            sector.draw(self._center, self._scale, cos_x, sin_x, cos_y, sin_y, self.surface)

    def draw_all_paths(self):
        for sector in self.sectors:
            for dest_sector in sector.lead_to:
                self._draw_line_between_sector(sector, dest_sector, (141, 105, 122), width=3)
                self._draw_line_between_sector(sector, dest_sector, (255, 236, 214), width=1)

    def draw_possible_paths(self):
        for dest_sector in self.current_sector.lead_to:
            self._draw_line_between_sector(self.current_sector, dest_sector, (141, 105, 122), width=5)
            self._draw_line_between_sector(self.current_sector, dest_sector, (255, 236, 214), width=3)

        if self.selected_sector:
            for dest_sector in self.selected_sector.lead_to:
                self._draw_line_between_sector(self.selected_sector, dest_sector, (141, 105, 122), width=4)
                self._draw_line_between_sector(self.selected_sector, dest_sector, (255, 236, 214), width=2)

    def draw_effects(self):

        # Draw current position indicator
        self.position_sprite.position = (self.current_sector.position[0],
                                         self.current_sector.position[1] - 17)
        self.position_sprite.raw_draw(self.surface, False)

        # Draw selected sector indicator
        self._select_state = (self._select_state + 0.1) % 4
        if self.selected_sector is not None:
            self.selection_sprites[int(self._select_state)].position = (self.selected_sector.position[0],
                                                                        self.selected_sector.position[1] - 17)

            self.selection_sprites[int(self._select_state)].raw_draw(self.surface, False)
