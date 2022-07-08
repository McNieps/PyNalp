import src.engine as engine

from src.game.menu_objects.play_button import play_sprite, play_button
from src.game.menu_objects.options_button import options_sprite, options_button
from src.game.menu_objects.about_button import about_sprite, about_button
from src.game.menu_objects.quit_button import quit_sprite, quit_button


import pygame

from pygame.locals import *


def menu():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI
    gui = engine.gui.GUI()
    gui.add_element(play_button)
    gui.add_element(options_button)
    gui.add_element(about_button)
    gui.add_element(quit_button)

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

        # region Compute

        # endregion

        # region Rendering
        screen.fill((0, 0, 0))

        # Draw GUI sprites (yes, this is ugly)
        play_sprite.raw_draw(screen)
        options_sprite.raw_draw(screen)
        about_sprite.raw_draw(screen)
        quit_sprite.raw_draw(screen)

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    menu()
    pygame.quit()
