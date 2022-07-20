import src.engine as engine

from src.game.menu_objects.buttons.utils import create_button, click_callback
from src.game.states.about import about

import pygame


def create_about_button():
    button_pos = 40, 160
    button_size = engine.resources.images["menu"]["button"].get_size()

    surf_up = pygame.Surface(button_size)
    surf_up.set_colorkey((0, 0, 0))
    surf_up.blit(engine.resources.images["menu"]["button"], (0, 0))
    surf_up.blit(engine.resources.images["menu"]["about"], (0, 0))

    about_button_dict = create_button(button_pos=button_pos,
                                      surf_up=surf_up,
                                      surf_down=surf_up,
                                      hover_callback=click_callback,
                                      pressed_callback=click_callback,
                                      released_callback=about)

    return about_button_dict
