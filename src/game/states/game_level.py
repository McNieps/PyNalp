if __name__ == '__main__':
    import os
    os.chdir("../../")

import src.engine as engine

from src.game.game_objects.player import Player
from src.game.game_objects.level import Level
from src.game.game_objects.wrap import Wrap
from src.game.states.loading_screen import loading_screen

import pygame

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

    wrap_distance = 20_000
    initial_wrap = Wrap(wrap_distance, 5)
    wrap = Wrap(wrap_distance, 2)
    initial_wrap.init_wrap()

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        # region Events
        key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_loop()
                if event.key == K_RETURN:
                    wrap.init_wrap()

        # endregion

        # region Computing
        wrap.compute(delta)
        initial_wrap.compute(delta)

        player.handle_key_pressed(key_pressed, delta)
        player.constrain()

        player_x, player_y = player.position

        dx, dy = player_x * player_camera_multiplier, player_y * player_camera_multiplier

        player.position[0] += wrap.distance + initial_wrap.distance
        camera.position = dx + wrap.distance + initial_wrap.distance, dy

        # endregion

        # region Rendering
        screen.fill((13, 43, 69))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)

        screen.blit(engine.resources.images["menu"]["frame"], (100, 100))

        # engine.shaders.GrayscaleShader.compute(screen)
        # engine.shaders.BlackHoleShader.compute(screen, 0.2)
        # engine.shaders.ChromaticAberrationShader.compute(screen, ((5, 5), (-5, 0), (5, -5)))

        screen.crop_border()

        screen.display.blit(engine.resources.images["enemies"]["kami_1"], (100, 100))
        screen.display.blit(engine.resources.images["enemies"]["sling_3"], (250, 150))
        pygame.draw.rect(screen.display, (255, 0, 0), (300, 124, 64, 64))

        pygame.display.flip()

        # endregion

        # region Post computing
        player.position[0] = player_x
        camera.position = player.position

        # endregion


if __name__ == '__main__':
    _player = Player()
    _level = Level(5)
    game_level(_player, _level)
    pygame.quit()
