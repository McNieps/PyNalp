"""
TODO explain how the game works, what assets I did end up using (like font, palette, ...), software
TODO explain that the easter exists / don't exists
"""

if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.menu_objects.return_button import return_button_dict
from src.game.menu_objects.utils import highlight_sprite

import pygame

from pygame.locals import *


def about():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # blur the screen
    engine.shaders.BlurShader.compute(screen, 2)
    engine.shaders.BlurShader.compute(screen, 2)

    # Initializing the GUI if necessary
    button_dicts = [return_button_dict]
    gui = engine.gui.GUI()
    gui.add_element(return_button_dict["button"])

    about_sprite = engine.scene.Sprite(resources.images["menu"]["about_page"], (200, 150))

    highlight_state = 0

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
        highlight_state = (highlight_state + delta*25) % 5

        # endregion

        # region Rendering

        about_sprite.raw_draw(screen)
        for button_dict in button_dicts:
            button_dict["sprite_down"].raw_draw(screen)
            if button_dict["button"].hovered:
                highlight_sprite(button_dict["sprite_up"], int(highlight_state))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    about()
    pygame.quit()
