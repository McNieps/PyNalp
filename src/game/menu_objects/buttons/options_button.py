import src.engine as engine

from src.game.menu_objects.buttons.utils import create_button, click_callback
from src.game.states.options import options

import pygame


button_pos = 40, 130
button_size = engine.resources.images["menu"]["button"].get_size()

surf_up = pygame.Surface(button_size)
surf_up.set_colorkey((0, 0, 0))
surf_up.blit(engine.resources.images["menu"]["button"], (0, 0))
surf_up.blit(engine.resources.images["menu"]["options"], (0, 0))

options_button_dict = create_button(button_pos=button_pos,
                                    surf_up=surf_up,
                                    surf_down=surf_up,
                                    hover_callback=click_callback,
                                    pressed_callback=click_callback,
                                    released_callback=options)
