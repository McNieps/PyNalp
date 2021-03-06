import src.engine as engine

import pygame


class Star:
    def __init__(self,
                 position: tuple[float, float, float],
                 sprite: engine.scene.Sprite):

        self.position = position
        self.sprite = sprite
        self.rect = sprite.rect

    def draw(self,
             center: list[int],
             scale: float,
             cos_x: float,
             sin_x: float,
             cos_y: float,
             sin_y: float,
             surface: pygame.Surface):

        x = cos_x * self.position[0] - sin_x * self.position[1]
        y = cos_y * self.position[2] + sin_y * (cos_x * self.position[1] + sin_x * self.position[0])
        self.rect.center = x, y

        self.sprite.position = x * scale + center[0], y * scale + center[1]
        self.sprite.raw_draw(surface, False)
