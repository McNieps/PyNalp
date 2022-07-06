import pygame
import numpy as np

from src.engine.shaders.abstract_shader import AbstractShader
from src.engine.typing import rect_style, surfarray_style


class ChromaticAberrationShader(AbstractShader):
    @classmethod
    def compute(cls,
                input_array: surfarray_style,
                rgb_dx_dy: tuple[tuple[int, int],
                                 tuple[int, int],
                                 tuple[int, int]],
                rect: rect_style = None,
                output_array: surfarray_style = None) -> None:
        """
        Method used to blur a spread R, G and B color channels.

        Args:
            input_array: A numpy array or a pygame surface that contain information to shade.
            rgb_dx_dy: A int representing the kernel radius. The kernel size is equal to 2*kernel_radius+1
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_array: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        if isinstance(input_array, pygame.Surface):
            input_array = pygame.surfarray.pixels3d(input_array)

        if output_array is None:
            output_array = input_array

        if rect is None:
            rect = (0, 0, *input_array.shape[:2])

        compute_chromatic_aberration(input_array, rgb_dx_dy, np.array(rect), output_array)


def compute_chromatic_aberration(input_array: np.ndarray,
                                 rgb_dx_dy: tuple[tuple[int, int],
                                                  tuple[int, int],
                                                  tuple[int, int]],
                                 rect: np.ndarray,
                                 output_array: np.ndarray) -> None:
    """ """

    size_x, size_y = input_array.shape[0:2]
    start_x = max(rect[0], 0)
    end_x = min(rect[0]+rect[2], size_x)
    start_y = max(rect[1], 0)
    end_y = min(rect[1]+rect[3], size_y)

    for c in range(3):
        if rgb_dx_dy[c]:
            output_array[start_x:end_x, start_y:end_y, c] = np.roll(input_array[start_x:end_x, start_y:end_y, c],
                                                                    rgb_dx_dy[c],
                                                                    (0, 1))
