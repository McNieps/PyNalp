import src.engine as engine
import src.test.utils as utils

import pygame

from pygame.locals import *


# Main loop function
def main():
    loop_handler = engine.loop_handler
    resources = engine.resources
    screen = engine.screen

    scene, camera = engine.scene.create_scene_and_camera()

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()
        pygame.display.set_caption(f"FPS: {loop_handler.get_fps()}")

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_game()

        utils.move_camera(camera, delta)

        # endregion

        # region Rendering
        screen.fill((0, 0, 0))
        camera.render_fixed_sprites(screen)

        screen.crop_border()
        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    engine.init("../../assets")
    main()
    pygame.quit()
