import src.engine as engine
import src.test.utils as utils

from src.engine.gui.typing import ValidMouseAction

import pygame

from pygame.locals import *


# Main loop function
def main():
    resources = engine.resources
    screen = engine.screen

    loop_handler = engine.handlers.LoopHandler()
    scene, camera = engine.scene.create_scene_and_camera()

    gui = engine.gui.GUI()
    buttons_sprites = []

    for i in range(1000):
        for j in range(5):
            button = engine.gui.Button(pressed_when_released=True, one_time_hover=True)
            button.position = (20 + i*40, 30 + j*60)

            button_sprite = engine.scene.Sprite(resources.images["misc"]["chti"], button.position)
            buttons_sprites.append(button_sprite)

            actions: list[ValidMouseAction] = ["hover", "pressed", "released"]
            for action in actions:
                button.set_mask_from_sprite(button_sprite, action)
                button.set_callback(resources.sounds["click"].play, action)

            gui.add_element(button)

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
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                gui.mouse_pressed()
            if event.type == MOUSEBUTTONUP and event.button == 1:
                gui.mouse_released()
        gui.update()

        utils.move_camera(camera, delta)

        # endregion

        # region Rendering
        screen.fill((255, 255, 255))
        camera.render_fixed_sprites(screen)

        for sprite in buttons_sprites:
            sprite.raw_draw(screen)

        screen.crop_border()

        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    main()
    pygame.quit()
