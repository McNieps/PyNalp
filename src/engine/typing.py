from src.engine.scene.sprites.classic_sprite import Sprite
from src.engine.scene.sprites.shader_sprite import ShaderSprite
from src.engine.scene.sprites.advanced_sprite import AdvancedSprite

import pygame
import numpy as np

from typing import Union


# Typing
rect_style = Union[pygame.Rect, tuple[int, int, int, int]]
sprite_style = Union[Sprite, ShaderSprite, AdvancedSprite]
surfarray_style = Union[pygame.Surface, np.ndarray]
