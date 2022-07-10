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

from src.game.game_objects.sector_selector.galaxy import Galaxy
from pygame.locals import *


def sector_selection():
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler
    galaxy = Galaxy()

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    background = engine.scene.Sprite(resources.images["sector_selection"]["background"], (200, 150))
    sprites_to_raw_draw = [background]

    # Animation variables
    anim_var = {"highlight": 0}

    mouse_pos = pygame.mouse.get_pos()

    # Main loop
    while loop_handler.is_running():
        print(loop_handler.get_fps())
        delta = loop_handler.limit_and_get_delta()

        # region Events
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

            elif event.type == MOUSEWHEEL:
                if event.y > 0:
                    for i in range(event.y):
                        galaxy.zoom(1.1)
                elif event.y < 0:
                    for i in range(abs(event.y)):
                        galaxy.zoom(1/1.1)

        key_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed(3)

        if key_pressed[K_LCTRL] and mouse_pressed[0]:
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
        blur_strength = 2
        engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)
        # engine.shaders.BlurShader.compute(galaxy_surf, blur_strength)
        galaxy.draw()

        screen.blit(galaxy_surf, (117, 140))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    sector_selection()
    pygame.quit()
