import src.engine as engine

from src.game.menu_objects.buttons import create_play_button, create_about_button, create_quit_button, highlight_sprite

import pygame

from pygame.locals import *
from math import cos, sin
from random import randint


def menu():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI
    button_dicts = [create_play_button(),
                    create_about_button(),
                    create_quit_button()]

    gui = engine.gui.GUI()
    for button_dict in button_dicts:
        gui.add_element(button_dict["button"])

    # Initializing menu sprites
    stars = []
    for star_type, nb in enumerate([50, 50, 50, 50]):
        for _ in range(nb):
            pos = randint(0, 400), randint(0, 260)
            star_sprite = engine.scene.Sprite(
                engine.resources.images["environment"][f"star_{star_type+1}_{randint(1, 3)}"], pos)

            stars.append(star_sprite)

    menu_warship = engine.scene.Sprite(resources.images["menu"]["warship"], (0, 0))
    menu_planet = engine.scene.Sprite(resources.images["menu"]["planet"], (200, 275))
    menu_clouds = engine.scene.Sprite(resources.images["menu"]["clouds"], (0, 0))
    menu_title = engine.scene.Sprite(resources.images["menu"]["title"], (200, 30))
    menu_reac_1 = engine.scene.Sprite(resources.images["menu"]["reac_1"], (0, 0))
    menu_reac_2 = engine.scene.Sprite(resources.images["menu"]["reac_1"], (0, 0))

    sprites_to_raw_draw = [*stars, menu_planet, menu_clouds, menu_title, menu_warship, menu_reac_1, menu_reac_2]

    anim_var = {"ship": 1,
                "clouds": 0,
                "highlight": 0,
                "reac_1": 1,
                "reac_2": 3}

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
        anim_var["ship"] = (anim_var["ship"] + delta) % 6.283
        menu_warship.position = int(168+12*cos(anim_var["ship"])), int(105 + 1*sin(anim_var["ship"]*3))

        anim_var["clouds"] = (anim_var["clouds"] + delta/5) % 6.283
        menu_clouds.position = 200+2*cos(anim_var["clouds"]*3), 285+2*sin(anim_var["clouds"])

        anim_var["highlight"] = (anim_var["highlight"] + delta*25) % 5

        anim_var["reac_1"] = (anim_var["reac_1"] + 16 * delta) % 5
        menu_reac_1.position = int(menu_warship.position[0] - 175), menu_warship.position[1] - 27
        menu_reac_1.surface = resources.images["menu"][f"reac_{int(anim_var['reac_1'])+1}"]

        anim_var["reac_2"] = (anim_var["reac_2"] + 16 * delta) % 5
        menu_reac_2.position = int(menu_warship.position[0] - 175), menu_warship.position[1] + 16
        menu_reac_2.surface = resources.images["menu"][f"reac_{int(anim_var['reac_2'])+1}"]

        # endregion

        # region Rendering
        screen.fill((13, 43, 69))

        # Drawing menu elements
        for sprite in sprites_to_raw_draw:
            sprite.raw_draw(screen)

        for button_dict in button_dicts:
            button_dict["sprite_down"].raw_draw(screen)
            if button_dict["button"].hovered:
                highlight_sprite(button_dict["sprite_up"], int(anim_var["highlight"]))

        screen.crop_border()
        screen.display.blit(engine.resources.images["menu"]["frame"], (0, 0))

        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    engine.init("../../../assets")
    menu()
    pygame.quit()
