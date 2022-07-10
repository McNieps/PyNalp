from src.game.game_objects.map.star import Star

import pygame

from typing import Iterable


class Sector:
    def __init__(self, num: int, depth: int, star: Star):
        self._num = num
        self._star = star
        self._depth = depth
        self._waves = []
        self.lead_to = []
        self.rect = star.rect

        self.position = self._star.position

    def add_destination(self, destination):
        self.lead_to.append(destination)

    def draw(self,
             center: Iterable[int],
             scale: float,
             cos_x: float,
             sin_x: float,
             cos_y: float,
             sin_y: float,
             surface: pygame.Surface):

        self._star.draw(center, scale, cos_x, sin_x, cos_y, sin_y, surface)
        self.rect.center = self._star.sprite.position
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
        self.position = self._star.sprite.position
