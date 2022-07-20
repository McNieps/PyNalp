"""
Illapsum Engine v0.0.1
Handle with care!
"""

__version__ = 'alpha.1'

import src.engine._hidden_utils as _utils
import src.engine.gui as gui
import src.engine.handlers as handlers
import src.engine.physics as physics
import src.engine.scene as scene
import src.engine.shaders as shaders
import src.engine.typing as utils

import pygame


# Welcome message!
print("Hello from the illapsum studio community. https://louis-thuillier.ac-amiens.fr/que-sont-ils-devenus/\n")

screen = None
loop_handler = handlers.LoopHandler
resources = handlers.ResourceHandler


def init(path: str = None):
    global screen

    resources.pre_init(path=path)

    # Setting up objects constants
    _utils.init()

    # Initializing pygame
    pygame.mixer.pre_init()
    pygame.init()

    # Create the window
    screen = _utils.create_screen(resources.data["sys"]["window"]["size"],
                                  resources.data["sys"]["window"]["name"],
                                  resources.data["sys"]["window"]["scaled"],
                                  resources.data["sys"]["window"]["fullscreen"])

    # Created the loop_handler

    # Finish resource_handler initialization
    handlers.ResourceHandler.init()
