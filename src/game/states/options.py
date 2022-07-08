"""
TODO must be able to change FPS, FULLSCREEN, Enable / Disable shaders, Volume
TODO create slider gui element TOUT SIMPLEMENT
"""

if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

import pygame

from pygame.locals import *


def options():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_game()

        # endregion

        # region Compute

        # endregion

        # region Rendering
        screen.fill((0, 0, 0))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    options()
    pygame.quit()
