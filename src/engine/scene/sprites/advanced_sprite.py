from src.engine.scene.sprites.abstract_sprite import AbstractSprite

import pygame

from typing import Union


class AdvancedSprite(AbstractSprite):
    __slots__ = ("surfaces", "angle")

    def __init__(self,
                 surfaces: Union[pygame.Surface, list[pygame.Surface]],
                 pos: tuple[int, int],
                 depth: float = 1,
                 raw_pos: tuple[float, float] = None):
        """

        """

        if isinstance(surfaces, pygame.Surface):
            surfaces = [surfaces]
        sprite_size = surfaces[0].get_size()

        super().__init__(sprite_size=sprite_size,
                         pos=pos,
                         depth=depth,
                         raw_pos=raw_pos)

        self.surfaces = surfaces
        self.angle = 0

    def draw(self,
             surface: pygame.Surface,
             position: tuple[int, int]) -> None:

        self.rect.center = position

        surf_to_blit = self.surfaces[0]

        if abs(self.angle) > 0.05:
            surf_to_blit = pygame.transform.rotate(surf_to_blit, self.angle)

        temp_rect = surf_to_blit.get_rect()
        temp_rect.center = position

        surface.blit(surf_to_blit, temp_rect)
