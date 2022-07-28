from src.engine.scene.typing import SpriteStyle
from src.engine.gui.typing import ValidMouseAction

import pygame
import numpy as np

from typing import Union


# Typing
RectStyle = Union[pygame.Rect, tuple[int, int, int, int]]
SurfArrayStyle = Union[pygame.Surface, np.ndarray]
