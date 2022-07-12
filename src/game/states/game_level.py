if __name__ == '__main__':
    import os
    os.chdir("../")

import src.engine as engine

from src.game.game_objects.player import Player
from src.game.game_objects.level import Level
from src.game.game_objects.wrap import Wrap
from src.game.states.loading_screen import loading_screen

import pygame
import math

from pygame.locals import *


def game_level(player, level):
    screen = engine.screen
    loop_handler = engine.loop_handler

    scene, camera = engine.scene.utils.create_scene_and_camera()
    scene.add_mobile_sprite(player.sprite)

    def add_stars_to_scene(list_of_stars: list, _scene: engine.scene.Scene):
        for star in list_of_stars:
            _scene.add_fixed_sprite(star)

    loading_screen(add_stars_to_scene, (level.stars, scene))

    player_camera_multiplier = 0.25
    wrap = Wrap(20000, 2)

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        key_pressed = pygame.key.get_pressed()
        button_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_loop()
                if event.key == K_RETURN:
                    wrap.init_wrap()

        # endregion

        wrap.compute(delta)

        player.handle_key_pressed(key_pressed, delta)
        player_x, player_y = player.position

        dx, dy = player_x * player_camera_multiplier, player_y * player_camera_multiplier

        player.position[0] += wrap.distance
        camera.position = dx + wrap.distance, dy

        # region Rendering
        screen.fill((13, 43, 69))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)

        player.position[0] = player_x
        camera.position = player.position

        screen.crop_border()
        screen.display.blit(engine.resources.images["menu"]["frame"], (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    _player = Player()
    _level = Level(5)
    game_level(_player, _level)
    pygame.quit()
