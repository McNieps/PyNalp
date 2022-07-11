if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

import pygame

from pygame.locals import *


def game_level(player, level):
    resources = engine.resources
    screen = engine.screen
    scene, camera = engine.scene.utils.create_scene_and_camera()

    loop_handler = engine.loop_handler

    # Initializing the GUI if necessary
    gui = engine.gui.GUI()

    anim_var = {"highlight": 0}

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_loop()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                gui.mouse_released()

        # endregion

        # region Compute
        gui.update()
        anim_var["highlight"] = (anim_var["highlight"] + delta*25) % 5

        # endregion

        # region Rendering
        screen.fill((13, 43, 69))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)
        screen.blit(resources.write("This is a level",
                                    (255, 255, 255),
                                    font_name="Square",
                                    font_size=45),
                    (100, 100))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    game_level(5, 5)
    pygame.quit()
