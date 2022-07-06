from src.engine.scene.typing import SpriteStyle
from src.engine.gui.typing import ValidMouseAction

import pygame
import numpy as np

from typing import Union


# Typing
rect_style = Union[pygame.Rect, tuple[int, int, int, int]]
surfarray_style = Union[pygame.Surface, np.ndarray]
