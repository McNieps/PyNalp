if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.game_objects.player import Player
from src.game.game_objects.level import Level
from src.test.utils import create_classic_sprites
from src.game.states.loading_screen import loading_screen

import pygame
import threading

from pygame.locals import *


def game_level(player, level):
    resources = engine.resources
    screen = engine.screen
    loop_handler = engine.loop_handler

    scene, camera = engine.scene.utils.create_scene_and_camera()
    scene.add_mobile_sprite(player.sprite)

    def add_stars_to_scene(list_of_stars: list, _scene: engine.scene.Scene):
        for star in list_of_stars:
            _scene.add_fixed_sprite(star)

    loading_screen(add_stars_to_scene, (level.stars, scene))

    # Main loop
    while loop_handler.is_running():
        print(loop_handler.get_fps())
        delta = loop_handler.limit_and_get_delta()

        # region Events
        key_pressed = pygame.key.get_pressed()
        button_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_loop()

        # endregion

        player.handle_key_pressed(key_pressed, delta)
        camera.position = player.position
        # print(int(camera.position[0]))

        # region Rendering
        screen.fill((13, 43, 69))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    _player = Player()
    _level = Level(5)
    game_level(_player, _level)
    pygame.quit()
