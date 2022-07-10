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

from src.game.game_objects.map.galaxy import Galaxy
from pygame.locals import *


def sector_selection(galaxy: Galaxy):
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    background = engine.scene.Sprite(resources.images["sector_selection"]["background"], (200, 150))
    sprites_to_raw_draw = [background]

    # Animation variables
    anim_var = {"highlight": 0}

    mouse_pos = pygame.mouse.get_pos()
    map_rect = pygame.Rect(17, 40, 236, 193)

    # Main loop
    while loop_handler.is_running():
        # print(loop_handler.get_fps())
        delta = loop_handler.limit_and_get_delta()

        # region Events
        key_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed(3)
        mouse_in_map = map_rect.collidepoint(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_loop()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()

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

        elif mouse_pressed[0]:
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
        gui.update()
        anim_var["highlight"] = (anim_var["highlight"] + delta*25) % 5
        galaxy.rotate(math.radians(5)*delta, 0)

        # endregion

        # region Rendering
        for sprite in sprites_to_raw_draw:
            sprite.raw_draw(screen)

        galaxy.surface.fill((13, 43, 69))
        # galaxy.surface.fill((255, 236, 214))

        galaxy_surf = galaxy.draw()
        blur_strength = 20
        engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)
        engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)

        galaxy.draw()
        galaxy.draw_accessible()
        galaxy.draw_paths()
        galaxy.draw_accessible()
        galaxy.draw_effects()

        screen.blit(galaxy_surf, (117, 140))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    _galaxy = Galaxy()
    sector_selection(_galaxy)
    pygame.quit()
