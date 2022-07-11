"""
This is just a template. There won't be any use for this script / module in the real game
Thanks buddy!
"""

if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.menu_objects.map import Galaxy

import pygame
import math

from pygame.locals import *


def sector_selection(galaxy: Galaxy):
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler
    gui = engine.gui.GUI()
    galaxy_surf = galaxy.surface
    galaxy_pos = galaxy.rect[0] + 100, galaxy.rect[1] + 100
    background = engine.scene.Sprite(resources.images["sector_selection"]["background"], (200, 150))
    sprites_to_raw_draw = [background]

    # Create button
    button_pos = 330, 259

    def pressed_callback():
        if galaxy.selected_sector is not None:
            engine.resources.play_sound(("click",))

    def released_callback():
        if galaxy.selected_sector is not None:
            loop_handler.stop_loop()

    button_up = engine.scene.Sprite(surface=engine.resources.images["sector_selection"]["launch_up"],
                                    position=button_pos)
    button_down = engine.scene.Sprite(surface=engine.resources.images["sector_selection"]["launch_down"],
                                      position=button_pos)
    button_locked = engine.scene.Sprite(surface=engine.resources.images["sector_selection"]["launch_locked"],
                                        position=button_pos)
    button = engine.gui.Button(button_pos)
    button.set_mask_from_sprite(button_up, "pressed")
    button.set_mask_from_sprite(button_down, "released")
    button.set_callback(pressed_callback, "pressed")
    button.set_callback(released_callback, "released")

    gui.add_element(button)

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
        galaxy.rotate(math.radians(1)*delta, 0)

        # endregion

        # region Rendering
        for sprite in sprites_to_raw_draw:
            sprite.raw_draw(screen)

        can_hover = not (key_pressed[K_LSHIFT] or key_pressed[K_LCTRL])
        galaxy.draw(can_hover, mouse_pos)

        screen.blit(galaxy_surf, galaxy_pos)

        if galaxy.selected_sector is None:
            button_locked.raw_draw(screen)
        elif button.pressed:
            button_down.raw_draw(screen)
        else:
            button_up.raw_draw(screen)

        screen.crop_border()
        pygame.display.flip()

    galaxy.current_sector = galaxy.selected_sector
    galaxy.selected_sector = None


if __name__ == '__main__':
    _galaxy = Galaxy()
    print(sector_selection(_galaxy))
    pygame.quit()
