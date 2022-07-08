import pygame
from src.engine.scene.sprites.abstract_sprite import AbstractSprite


class Sprite(AbstractSprite):
    __slots__ = ("surface",)

    def __init__(self,
                 surface: pygame.Surface,
                 position: tuple[float, float],
                 depth: float = 1,
                 raw_pos: tuple[float, float] = None) -> None:
        """
        Class used to create static sprites inside a 2d environment (scene submodule)

        Args:
            surface: the surface of the sprite
            position: True position (overlap with camera when camera coords = pos)
            depth: Depth of the sprite (0: don't move, 1: move along the plan, 2: move twice as fast, etc.)
            raw_pos: Initial offset from origin
            """

        super().__init__(surface.get_rect().size, position, depth, raw_pos)

        self.surface = surface

    def draw(self,
             surface: pygame.Surface,
             position: tuple[int, int]) -> None:
        """
        Method used to draw the sprite. Should only be called by the camera.
        Or you, if you can correctly calculate the position!

        Args:
            surface: The surface the sprite should be blit on.
            position: The center where the sprite should be blit.
        """
        self.rect.center = position

        surface.blit(self.surface, self.rect)

    def raw_draw(self,
                 surface: pygame.Surface,
                 offset_shaders: bool = True) -> None:
        """
        Method used to draw the sprite.

        Args:
            surface: The surface the sprite should be blit on.
            offset_shaders: If True, offset the blit pos to account for the shader margin.
        """

        if offset_shaders:
            pos = (self.position[0]+self._DISPLAY_RECT[0]-self.half_size[0],
                   self.position[1]+self._DISPLAY_RECT[1]-self.half_size[1])
        else:
            pos = (self.position[0]-self.half_size[0],
                   self.position[1]-self.half_size[1])

        surface.blit(self.surface, pos)
