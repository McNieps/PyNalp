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


def init(resource_handler: handlers.ResourceHandler):
    shaders_max_size = resource_handler.fetch_data(["sys", "shaders", "max_size"])
    shaders_enabled = resource_handler.fetch_data(["sys", "shaders", "enabled"])
    if shaders_enabled is not True:
        shaders_max_size = 0

    init_gui(resource_handler)
    init_handlers(resource_handler)
    init_physics(resource_handler)
    init_scene(resource_handler)
    init_shaders(resource_handler)

    # Screen constants
    Screen.SHADERS_ENABLED = shaders_enabled
    Screen.SHADERS_MAX_SIZE = shaders_max_size


def init_gui(resource_handler: handlers.ResourceHandler):
    """Init gui objects."""

    pass


def init_handlers(resource_handler: handlers.ResourceHandler):
    """Init handlers objects."""

    # LoopHandler constants
    handlers.LoopHandler.MAX_FPS = resource_handler.fetch_data(["sys", "video", "fps"])


def init_physics(resource_handler: handlers.ResourceHandler):
    """Init physics objects."""

    pass


def init_scene(resource_handler: handlers.ResourceHandler):
    screen_size = resource_handler.fetch_data(["sys", "window", "size"])
    shaders_max_size = resource_handler.fetch_data(["sys", "shaders", "max_size"])
    shaders_enabled = resource_handler.fetch_data(["sys", "shaders", "enabled"])

    # Scene object
    scene.Scene._SCREEN_SIZE = resource_handler.fetch_data(["sys", "window", "size"])
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
    AbstractSprite._SCREEN_RECT = screen_rect

    # ShaderSprite object
    scene.ShaderSprite.DISPLAY_RECT = pygame.Rect(0,
                                                  0,
                                                  screen_size[0]+shaders_max_size*2,
                                                  screen_size[1]+shaders_max_size*2)


def init_shaders(resource_handler: handlers.ResourceHandler):
    resource_handler.shaders = {"blackhole": shaders.BlackHoleShader,
                                "blur": shaders.BlurShader,
                                "chromatic": shaders.ChromaticAberrationShader,
                                "grayscale": shaders.GrayscaleShader}
