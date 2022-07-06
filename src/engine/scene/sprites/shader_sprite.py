from src.engine.scene.sprites.abstract_sprite import AbstractSprite

from typing import Any

import pygame


class ShaderSprite(AbstractSprite):
    __slots__ = ("shader", "shader_value")

    SHADER_MAX_SIZE = 100
    DISPLAY_RECT = pygame.Rect(0, 0, 0, 0)

    def __init__(self,
                 shader,
                 shader_value: Any,
                 shader_size: tuple[int, int],
                 pos: tuple[float, float],
                 depth: float,
                 raw_pos: tuple[float, float] = None,
                 fixed_size: bool = True) -> None:
        """
        Class used to create shader sprites inside a 2d environment (scene submodule)

        Args:
            shader: the shader to apply to the scene.
            shader_value: A argument that may change from one shader to another. No defined type.
            shader_size: Shader size.
            pos: True position (overlap with camera when camera coords = pos).
            raw_pos: Initial offset from origin.
            depth: Depth of the sprite (0: don't move, 1: move along the plan, 2: move twice as fast, etc.
                CAN BE NEGATIVE).
            fixed_size: If True: modifying the sprite size may lead to problems.
        """

        size = shader_size
        if not fixed_size:
            size = self.SHADER_MAX_SIZE*2, self.SHADER_MAX_SIZE*2

        super().__init__(size, pos, depth, raw_pos)

        self.shader = shader
        self.shader_value = shader_value

    @property
    def shader_size(self):
        return self.rect.size

    @shader_size.setter
    def shader_size(self, value):
        self.rect.size = value

    def draw(self,
             surface: pygame.Surface,
             position: tuple[int, int]) -> None:

        self.rect.center = position

        if not self.DISPLAY_RECT.contains(self.rect):
            return

        sub_surface = surface.subsurface(self.rect)  # negligible
        sub_array = pygame.surfarray.pixels3d(sub_surface)  # negligible

        self.shader.compute(sub_array, self.shader_value)  # TODO rework this
