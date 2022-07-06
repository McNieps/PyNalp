from src.engine.shaders.abstract_shader import AbstractShader
from src.engine.typing import rect_style, surfarray_style

import pygame
import numpy as np

from numba import njit, prange
from typing import Tuple


class GrayscaleShader(AbstractShader):
    @classmethod
    def compute(cls,
                input_array: surfarray_style,
                weights: Tuple[float, float, float] = (0.3, 0.59, 0.11),
                rect: rect_style = None,
                output_array: np.ndarray = None) -> None:
        """
        Method used to grayscale a surface.

        Args:
            input_array: A numpy array or a pygame surface that contain information to shade.
            weights: A tuple containing 3 float (one for each color). intensity = w[0]*r + w[1]*g + w[2]*b.
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_array: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        if isinstance(input_array, pygame.Surface):
            input_array = pygame.surfarray.pixels3d(input_array)

        if rect is None:
            rect = (0, 0, *input_array.shape[:2])

        if output_array is None:
            output_array = input_array

        compute_grayscale(input_array=input_array,
                          weights=np.array(weights),
                          rect=np.array(rect),
                          output_array=output_array)


@njit(fastmath=True, cache=True, parallel=True)
def compute_grayscale(input_array: np.ndarray,
                      weights: np.ndarray,
                      rect: np.ndarray,
                      output_array: np.ndarray) -> None:
    """0.5 ms for 600*500 surface, 0.13 ms for 400*300 surface"""

    size_x, size_y = input_array.shape[:2]
    start_x = max(rect[0], 0)
    end_x = min(rect[0] + rect[2], size_x)
    start_y = max(rect[1], 0)
    end_y = min(rect[1] + rect[3], size_y)

    r_map = np.empty(256, dtype='uint8')
    g_map = np.empty(256, dtype='uint8')
    b_map = np.empty(256, dtype='uint8')

    for k in range(256):
        r_map[k] = k * weights[0]
        g_map[k] = k * weights[1]
        b_map[k] = k * weights[2]

    for i in prange(start_x, end_x):
        for j in range(start_y, end_y):
            val = r_map[input_array[i, j, 0]] + \
                  g_map[input_array[i, j, 1]] + \
                  b_map[input_array[i, j, 2]]

            for channel in range(3):
                output_array[i, j, channel] = val
