if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.menu_objects.buttons.return_button import create_return_button
from src.game.menu_objects.buttons.utils import highlight_sprite

import pygame

from pygame.locals import *


def about():
    loop_handler = engine.loop_handler
    resources = engine.resources
    screen = engine.screen

    # blur the screen
    engine.shaders.BlurShader.shade(screen, 2)
    engine.shaders.BlurShader.shade(screen, 2)

    # Initializing the GUI if necessary
    button_dicts = [create_return_button()]
    gui = engine.gui.GUI()
    gui.add_element(button_dicts[0]["button"])

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
