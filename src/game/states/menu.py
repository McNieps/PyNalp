if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.menu_objects.play_button import play_button_dict
from src.game.menu_objects.options_button import options_button_dict
from src.game.menu_objects.about_button import about_button_dict
from src.game.menu_objects.quit_button import quit_button_dict

import pygame

from pygame.locals import *


def menu():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI
    button_dicts = [play_button_dict,
                    options_button_dict,
                    about_button_dict,
                    quit_button_dict]

    gui = engine.gui.GUI()
    for button_dict in button_dicts:
        gui.add_element(button_dict["button"])

    # Initializing menu sprites
    menu_background = engine.scene.Sprite(resources.images["space"], (200, 150))
    menu_warship = engine.scene.Sprite(resources.images["menu"]["warship"], (200, 150))
    menu_planet = engine.scene.Sprite(resources.images["menu"]["planet"], (200, 285))
    sprites_to_raw_draw = [menu_background, menu_warship, menu_planet]

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
        gui.update()

        # endregion

        # region Rendering
        screen.fill((32, 60, 86))

        # Drawing menu elements
        for sprite in sprites_to_raw_draw:
            sprite.raw_draw(screen)

        for button_dict in button_dicts:
            if button_dict["button"].pressed:
                button_dict["sprite_down"].raw_draw(screen)
            else:
                button_dict["sprite_up"].raw_draw(screen)

        screen.crop_border()
        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    menu()
    pygame.quit()
