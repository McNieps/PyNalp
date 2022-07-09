"""
This is just a template. There won't be any use for this script / module in the real game
Thanks buddy!
"""

if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

import pygame

from pygame.locals import *


def template():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    highlight_state = 0

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_game()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                gui.mouse_released()

        # endregion

        # region Compute
        gui.update()
        highlight_state = (highlight_state + delta*25) % 5

        # endregion

        # region Rendering
        screen.fill((0, 0, 0))

        screen.blit(resources.write("This is a template",
                                    (255, 255, 255),
                                    font_name="Square",
                                    font_size=45),
                    (100, 100))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    template()
    pygame.quit()
