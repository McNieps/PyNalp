import src.engine as engine

import pygame

from typing import Callable


def highlight_sprite(sprite_to_highlight: engine.scene.Sprite,
                     state: int) -> None:

    hl_sprite = engine.scene.Sprite(engine.resources.images["menu"][f"hl_{state+1}"], (0, 0))

    hl_sprite.position = sprite_to_highlight.position
    hl_sprite.raw_draw(engine.screen)


def click_callback():
    engine.resources.play_sound(("click",))


def create_button(button_pos: tuple[int, int],
                  surf_up: pygame.Surface,
                  surf_down: pygame.Surface,
                  hover_callback: Callable,
                  pressed_callback: Callable,
                  released_callback: Callable) -> dict:

    sprite_up = engine.scene.Sprite(surface=surf_up,
                                    position=button_pos)

    sprite_down = engine.scene.Sprite(surface=surf_down,
                                      position=button_pos)

    button = engine.gui.Button(button_pos)

    # Setting button callbacks
    button.set_callback(hover_callback, "hover")
    button.set_callback(pressed_callback, "pressed")
    button.set_callback(released_callback, "released")

    # Setting button rect / mask
    button.set_mask_from_sprite(sprite_up, "hover")
    button.set_mask_from_sprite(sprite_up, "pressed")
    button.set_mask_from_sprite(sprite_down, "released")

    button_dict = {"button": button,
                   "sprite_up": sprite_up,
                   "sprite_down": sprite_down}

    return button_dict
