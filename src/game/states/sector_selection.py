"""
This is just a template. There won't be any use for this script / module in the real game
Thanks buddy!
"""

if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

import pygame
import math

from src.game.menu_objects.map import Galaxy
from pygame.locals import *


def sector_selection(galaxy: Galaxy):
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler
    gui = engine.gui.GUI()

    galaxy_surf = galaxy.surface
    background = engine.scene.Sprite(resources.images["sector_selection"]["background"], (200, 150))
    sprites_to_raw_draw = [background]

    # Animation variables
    anim_var = {"highlight": 0,
                "position": 5}

    mouse_pos = pygame.mouse.get_pos()
    map_rect = pygame.Rect(17, 40, 236, 193)

    # Main loop
    while loop_handler.is_running():
        # print(loop_handler.get_fps())
        delta = loop_handler.limit_and_get_delta()

        # region Events
        key_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed(3)
        mouse_just_pressed = False
        mouse_in_map = map_rect.collidepoint(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_loop()
                if event.key == K_r:
                    galaxy.reset()
                if event.key == K_RETURN and galaxy.selected_sector is not None:
                    loop_handler.stop_loop()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()
                mouse_just_pressed = True

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                gui.mouse_released()

            elif mouse_in_map and event.type == MOUSEWHEEL:
                if event.y > 0:
                    for i in range(event.y):
                        galaxy.zoom(1.1)
                elif event.y < 0:
                    for i in range(abs(event.y)):
                        galaxy.zoom(1/1.1)

        if not mouse_in_map:
            mouse_pos = pygame.mouse.get_pos()

        elif key_pressed[K_LCTRL] and mouse_pressed[0]:
            new_mouse_pos = pygame.mouse.get_pos()
            dx, dy = new_mouse_pos[0] - mouse_pos[0], new_mouse_pos[1] - mouse_pos[1]
            galaxy.rotate(math.radians(dx), math.radians(dy))
            mouse_pos = new_mouse_pos

        elif key_pressed[K_LSHIFT] and mouse_pressed[0]:
            new_mouse_pos = pygame.mouse.get_pos()
            dx, dy = mouse_pos[0] - new_mouse_pos[0], mouse_pos[1] - new_mouse_pos[1]
            galaxy.move(dx, dy, False)
            mouse_pos = new_mouse_pos

        elif mouse_pressed[2]:
            new_mouse_pos = pygame.mouse.get_pos()
            dx, dy = new_mouse_pos[0] - mouse_pos[0], new_mouse_pos[1] - mouse_pos[1]
            galaxy.rotate(math.radians(dx * delta), math.radians(dy * delta))

        else:
            mouse_pos = pygame.mouse.get_pos()

        # endregion

        # region Compute
        if mouse_just_pressed and not (key_pressed[K_LCTRL] or key_pressed[K_LSHIFT]):
            galaxy.click(mouse_pos)

        gui.update()

        anim_var["highlight"] = (anim_var["highlight"] + delta*25) % 5
        galaxy.rotate(math.radians(5)*delta, 0)

        # endregion

        # region Rendering
        for sprite in sprites_to_raw_draw:
            sprite.raw_draw(screen)

        galaxy.draw_background()
        galaxy.draw_galaxy()

        # Applying shader for 'bloom'. Comment this code if slow
        blur_strength = 16
        engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)
        engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)
        galaxy.draw_galaxy()
        # Comment till here.

        galaxy.draw_all_paths()

        if not (key_pressed[K_LCTRL] or key_pressed[K_LSHIFT]):
            galaxy.hover(mouse_pos)

        galaxy.draw_possible_paths()    # Draw current possibles paths and selected sector possibles paths
        galaxy.draw_accessible()        # Draw sectors

        galaxy.draw_effects()

        screen.blit(galaxy_surf, (117, 140))

        screen.crop_border()
        pygame.display.flip()

    galaxy.current_sector = galaxy.selected_sector
    galaxy.selected_sector = None


if __name__ == '__main__':
    _galaxy = Galaxy()
    print(sector_selection(_galaxy))
    pygame.quit()
