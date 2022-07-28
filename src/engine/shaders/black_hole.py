from src.engine.shaders.abstract_shader import AbstractShader
from src.engine.typing import SurfArrayStyle, RectStyle

import numpy as np

from itertools import product
from numba import njit, prange
from typing import Iterable


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


@njit(parallel=True, fastmath=True, cache=True)
def compute_black_hole(input_array: np.ndarray,
                       shader_map: np.ndarray,
                       zone: np.ndarray,
                       output_array: np.ndarray) -> None:

    if input_array is output_array:
        input_array = input_array.copy()

    print(shader_map.shape)
    print(shader_map.dtype)

    size = shader_map.shape[0]
    start_x = max(0, min(zone[0], size))
    start_y = max(0, min(zone[1], size))
    end_x = max(0, min(zone[0] + zone[2], size))
    end_y = max(0, min(zone[1] + zone[3], size))
    print(size)
    print(start_x)
    print(start_y)
    print(end_x)
    print(end_y)
    print(zone)

    input_array = input_array[start_x: end_x, start_y: end_y]
    output_array = output_array[start_x: end_x, start_y: end_y]

    for i in prange(size):
        for j in range(size):
            nx = shader_map[i, j, 0]
            ny = shader_map[i, j, 1]
            output_array[i, j] = input_array[nx, ny]


class BlackHoleShader(AbstractShader):
    INIT_VALUE = create_shader_map(10, 1)
    FUNC = compute_black_hole

    INTENSITY_DECIMAL_PRECISION = 1
    shader_maps: dict[tuple[int, float], np.ndarray] = {}

    @classmethod
    def shade(cls,
              input_surfarray: SurfArrayStyle,
              intensity: float,
              rect: RectStyle = None,
              output_surfarray: SurfArrayStyle = None):
        """
        Method used to distort the surface, making it blackhole style

        Args:
            input_surfarray: A numpy array or a pygame surface that contain information to shade.
            intensity: If 0 then Nothing. If in ]-1, 0[ then sucking effect. If > 0 then black hole.
            rect: The size of the black hole is defined by the min(rect.width, rect.height).
                The center of the black hole is the center of the rect.
            output_surfarray: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        input_array, _, rect_array, output_array = cls._adapt_args(input_surfarray=input_surfarray,
                                                                   values=None,
                                                                   rect=rect,
                                                                   output_surfarray=output_surfarray)

        intensity = round(intensity, cls.INTENSITY_DECIMAL_PRECISION)

        size = min(*rect_array[2:])

        # rect_array[0] += (rect_array[2]-size)/2
        # rect_array[1] += (rect_array[3]-size)/2
        rect_array[2:] = size

        shader_map = cls._get_shader_map(size, intensity)

        cls._compute(input_array=input_array,
                     values=shader_map,
                     rect_array=rect_array,
                     output_array=output_array)

    @classmethod
    def _get_shader_map(cls,
                        size: int,
                        intensity: float) -> np.ndarray:
        """Return a shader map with specific size and intensity. If the shader map doesn't exist yet, create it."""

        shader_map_key = (size, intensity)

        if shader_map_key not in cls.shader_maps:
            cls.shader_maps[shader_map_key] = create_shader_map(size, intensity)

        return cls.shader_maps[shader_map_key]

    @classmethod
    def pre_gen_shader_map(cls,
                           size: Iterable[int] | int,
                           intensity: Iterable[float] | float) -> None:
        """Used to pre-compute shader maps"""

        if size is int:
            size = [size]

        if intensity is float:
            intensity = [intensity]

        iterator = list(product(size, intensity))

        for s, i in iterator:
            cls._get_shader_map(s, i)
