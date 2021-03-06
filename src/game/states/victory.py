"""
This is just a template. There won't be any use for this script / module in the real game
Thanks buddy!
"""

if __name__ == '__main__':
    import os
    os.chdir("../../")

import src.engine as engine

import pygame

from pygame.locals import *


def victory():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    victory_sprite = engine.scene.Sprite(resources.images["menu"]["victory"], (200, 150))

    anim_var = {"highlight": 0}

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_loop()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                gui.mouse_released()

        # endregion

        # region Compute
        gui.update()
        anim_var["highlight"] = (anim_var["highlight"] + delta*25) % 5

        # endregion

        # region Rendering

        screen.fill((13, 43, 69))
        victory_sprite.raw_draw(screen)

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    victory()
    pygame.quit()
