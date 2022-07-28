import src.engine.gui as gui
import src.engine.handlers as handlers
import src.engine.physics as physics
import src.engine.scene as scene
import src.engine.shaders as shaders

from src.engine.scene.sprites.abstract_sprite import AbstractSprite
from src.engine.screen import Screen

import pygame


def create_screen(size: tuple[int, int],
                  window_name: str,
                  scaled: bool,
                  fullscreen: bool) -> Screen:
    """Function used to create window screen"""

    flags = (scaled * pygame.SCALED) | (fullscreen * pygame.FULLSCREEN)
    window = pygame.display.set_mode(size, flags=flags)

    if window_name:
        pygame.display.set_caption(window_name)

    screen = Screen(window)

    return screen


def init():
    shaders_max_size = handlers.ResourceHandler.data["sys"]["shaders"]["max_size"]
    shaders_enabled = handlers.ResourceHandler.data["sys"]["shaders"]["enabled"]
    if shaders_enabled is not True:
        shaders_max_size = 0

    init_gui()
    init_handlers()
    init_physics()
    init_scene()
    init_shaders()

    # Screen constants
    Screen.SHADERS_ENABLED = shaders_enabled
    Screen.SHADERS_MAX_SIZE = shaders_max_size


def init_gui():
    """Init gui objects."""

    screen_size = handlers.ResourceHandler.data["sys"]["window"]["size"]
    shaders_max_size = handlers.ResourceHandler.data["sys"]["shaders"]["max_size"]
    shaders_enabled = handlers.ResourceHandler.data["sys"]["shaders"]["enabled"]

    if shaders_enabled:
        gui.Button._DISPLAY_RECT = pygame.Rect(shaders_max_size, shaders_max_size, *screen_size)


def init_handlers():
    """Init handlers objects."""

    # LoopHandler constants
    handlers.LoopHandler.max_fps = handlers.ResourceHandler.data["sys"]["video"]["fps"]


def init_physics():
    """Init physics objects."""

    pass


def init_scene():
    """Init scene objects."""
    screen_size: tuple[int, int] = handlers.ResourceHandler.data["sys"]["window"]["size"]
    shaders_max_size: int = handlers.ResourceHandler.data["sys"]["shaders"]["max_size"]
    shaders_enabled: bool = handlers.ResourceHandler.data["sys"]["shaders"]["enabled"]

    # Scene object
    scene.Scene._SCREEN_SIZE = handlers.ResourceHandler.data["sys"]["window"]["size"]
    scene.Scene._INV_SCREEN_SIZE = (1 / screen_size[0],
                                    1 / screen_size[1])
    scene.Scene._SHADERS_ENABLED = shaders_enabled

    # Camera object
    scene.Camera._SCREEN_SIZE = screen_size

    if shaders_enabled:
        scene.Camera._BLIT_OFFSET = (screen_size[0] / 2 + shaders_max_size,
                                     screen_size[1] / 2 + shaders_max_size)
        scene.Camera._SHADER_MAX_SIZE = shaders_max_size

    else:
        scene.Camera._BLIT_OFFSET = (screen_size[0] / 2,
                                     screen_size[1] / 2)

    # Sprite object (all of them in fact)
    screen_rect = pygame.Rect(0, 0, screen_size[0]+shaders_max_size*2, screen_size[1]+shaders_max_size*2)
    display_rect = pygame.Rect(shaders_max_size, shaders_max_size, *screen_size)

    AbstractSprite._SCREEN_RECT = screen_rect
    AbstractSprite._DISPLAY_RECT = display_rect

    # ShaderSprite object
    scene.ShaderSprite.DISPLAY_RECT = pygame.Rect(0,
                                                  0,
                                                  screen_size[0]+shaders_max_size*2,
                                                  screen_size[1]+shaders_max_size*2)


def init_shaders():
    """Init shaders objects."""
    pass
