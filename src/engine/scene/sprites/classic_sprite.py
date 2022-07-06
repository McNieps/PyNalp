import pygame
from src.engine.scene.sprites.abstract_sprite import AbstractSprite


class Sprite(AbstractSprite):
    __slots__ = ("surface",)

    def __init__(self,
                 surface: pygame.Surface,
                 pos: tuple[float, float],
                 depth: float = 1,
                 raw_pos: tuple[float, float] = None) -> None:
        """
        Class used to create static sprites inside a 2d environment (scene submodule)

        Args:
            surface: the surface of the sprite
            pos: True position (overlap with camera when camera coords = pos)
            depth: Depth of the sprite (0: don't move, 1: move along the plan, 2: move twice as fast, etc.)
            raw_pos: Initial offset from origin
            """

        super().__init__(surface.get_rect().size, pos, depth, raw_pos)

        self.surface = surface

    def draw(self,
             surface: pygame.Surface,
             position: tuple[int, int]) -> None:

        self.rect.center = position

        surface.blit(self.surface, self.rect)
