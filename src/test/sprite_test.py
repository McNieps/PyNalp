import src.engine as engine
import src.test.utils as utils

import pygame

from pygame.locals import *


# Main loop function
def main():
    resources = engine.resources
    screen = engine.screen

    loop_handler = engine.handlers.LoopHandler()
    scene, camera = engine.scene.create_scene_and_camera()

    # Add stars to the scene and order them
    utils.create_classic_sprites(scene)
    frog = engine.scene.Sprite(resources.images["misc"]["frog"], (0, 0), depth=0.4)
    scene.add_fixed_sprite(frog)
    scene.order()

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

        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_KP4]:
            frog.x -= 500 * delta
        if key_pressed[K_KP6]:
            frog.x += 500 * delta
        if key_pressed[K_KP8]:
            frog.y -= 500 * delta
        if key_pressed[K_KP5]:
            frog.y += 500 * delta
        # endregion

        # region Rendering
        screen.fill((0, 0, 0))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)
        camera.draw_active_cluster(screen, (255, 255, 255))
        screen.crop_border()
        # screen.show_all()
        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    engine.init("../../assets")
    main()
    pygame.quit()
