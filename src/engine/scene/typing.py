from src.engine.scene.sprites.classic_sprite import Sprite
from src.engine.scene.sprites.shader_sprite import ShaderSprite
from src.engine.scene.sprites.advanced_sprite import AdvancedSprite

from typing import Union


SpriteStyle = Union[Sprite, ShaderSprite, AdvancedSprite]
