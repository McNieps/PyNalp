import src.engine as engine

import pygame

from pygame.locals import *
from random import randint


def create_classic_sprites(_scene: engine.scene.Scene,
                           _resources: engine.handlers.ResourceHandler,
                           background_image: bool = True) -> None:
    """Add some sprites to the scene to make it looks like space..."""

    sprite_nb = 1000
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000
    min_d, max_d = 0, 2

    # Adding background image
    if background_image:
        _scene.add_fixed_sprite(engine.scene.Sprite(_resources.images["misc"]["space"], (0, 0), 0))

    # Adding small stars here and there...
    for _ in range(sprite_nb):
        surface = _resources.images["cursors"][f"cursor_{randint(1, 6)}"]
        pos = randint(min_x, max_x), randint(min_y, max_y)
        depth = randint(min_d*10000, max_d*10000) / 10000
        raw_pos = randint(-200, 200), randint(-150, 150)

        new_sprite = engine.scene.Sprite(surface=surface, position=pos, depth=depth, raw_pos=raw_pos)

        _scene.add_fixed_sprite(new_sprite)


def move_camera(_camera: engine.scene.Camera,
                delta: float) -> None:
    """Move the camera"""

    camera_speed = 500
    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_z]:
        _camera.y -= camera_speed * delta
    elif key_pressed[K_s]:
        _camera.y += camera_speed * delta
    if key_pressed[K_q]:
        _camera.x -= camera_speed * delta
    elif key_pressed[K_d]:
        _camera.x += camera_speed * delta
