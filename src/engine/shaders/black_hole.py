from src.engine.shaders.abstract_shader import AbstractShader
from src.engine.typing import surfarray_style, rect_style

import pygame
import numpy as np

from itertools import product
from numba import njit, prange
from typing import Iterable


class BlackHoleShader(AbstractShader):
    DECIMAL_VALUES = 1
    shader_maps = {}

    @classmethod
    def get_shader_map(cls,
                       size: int,
                       intensity: float) -> np.ndarray:
        """Return a shader map with specific size and intensity. If the shader map doesn't exist yet, create it."""

        shader_map_key = (size, intensity)

        if shader_map_key not in cls.shader_maps:
            cls.shader_maps[shader_map_key] = create_shader_map(size, intensity)

        return cls.shader_maps[shader_map_key]

    @classmethod
    def pre_gen_shader_map(cls,
                           size: Iterable[int],
                           intensity: Iterable[float]) -> None:
        """Used to pre-compute shader maps"""

        iterator = list(product(size, intensity))

        for s, i in iterator:
            cls.get_shader_map(s, i)

    @classmethod
    def compute(cls,
                input_array: surfarray_style,
                intensity: float,
                rect: rect_style = None,
                output_array: surfarray_style = None) -> None:
        """ """

        if isinstance(input_array, pygame.Surface):
            input_array = pygame.surfarray.pixels3d(input_array)

        if output_array is None:
            output_array = input_array

        if rect is None:
            rect = pygame.Rect(0, 0, *input_array.shape[:2])

        center = rect.center
        size = min(*rect.size)

        rect = pygame.Rect(0, 0, size, size)
        rect.center = center

        intensity = round(intensity, cls.DECIMAL_VALUES)

        shader_map = cls.get_shader_map(size, intensity)

        compute_black_hole(input_array=input_array,
                           shader_map=shader_map,
                           zone=np.array(rect),
                           output_array=output_array)


@njit(parallel=True, fastmath=True, cache=True)
def create_shader_map(size: int,
                      intensity: float) -> np.ndarray:

    radius = int(size / 2)
    swap_map = np.sin(np.linspace(0, 1, radius) * np.pi / 2) ** intensity * 2 - 1

    shader_map = np.empty((size, size, 2), dtype="uint16")

    for i in prange(size):
        for j in range(size):
            dx, dy = i - radius, j - radius
            dist = int(np.hypot(dx, dy))

            if dist >= radius or dist == 0:
                shader_map[i][j] = np.array((i, j))
                continue

            nx, ny = int(dx * swap_map[dist] + radius), int(dy * swap_map[dist] + radius)
            shader_map[i][j] = np.array((nx, ny))

    return shader_map


@njit(parallel=True, cache=True)
def compute_black_hole(input_array: np.ndarray,
                       shader_map: np.ndarray,
                       zone: np.ndarray,
                       output_array: np.ndarray) -> None:

    if input_array is output_array:
        input_array = input_array.copy()

    size = shader_map.shape[0]
    start_x = max(0, min(zone[0], size))
    start_y = max(0, min(zone[1], size))
    end_x = max(0, min(zone[0] + zone[2], size))
    end_y = max(0, min(zone[1] + zone[3], size))

    input_array = input_array[start_x: end_x, start_y: end_y]
    output_array = output_array[start_x: end_x, start_y: end_y]

    for i in prange(size):
        for j in range(size):
            nx = shader_map[i, j, 0]
            ny = shader_map[i, j, 1]
            output_array[i, j] = input_array[nx, ny]
