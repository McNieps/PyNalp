if __name__ == '__main__':
    import os
    os.chdir("../../")

import src.engine as engine

from src.game.game_objects.player import Player
from src.game.game_objects.level import Level
from src.game.game_objects.wrap import Wrap
from src.game.game_objects.bullet import Bullet
from src.game.game_objects.enemies.enemy import Enemy
from src.game.game_objects.enemies.kami import Kami
from src.game.game_objects.enemies.beholder import Beholder

from src.game.states.loading_screen import loading_screen

import pygame

from pygame.locals import *


def game_level(player, level):
    screen = engine.screen
    loop_handler = engine.loop_handler

    scene, camera = engine.scene.utils.create_scene_and_camera()
    scene.add_mobile_sprite(player.sprite)

    Bullet.SCENE = scene
    Enemy.SCENE = scene

    level.generate_level()

    def add_stars_to_scene(list_of_stars: list, _scene: engine.scene.Scene):
        for star in list_of_stars:
            _scene.add_fixed_sprite(star)

    loading_screen(add_stars_to_scene, (level.stars, scene))

    player_camera_multiplier = 0.25

    # wrap
    initial_wrap = Wrap(20_000, 0.2)
    wrap = Wrap(20_000, 2)
    initial_wrap.init_wrap()
    wrap_delay_after_wave_end = 2
    time_to_next_wave = 0
    time_to_wave = 0
    wave_wait_after_wrap = 1
    wave_launched = False
    current_wave = 0

    # arena
    arena_rect = pygame.Rect(0, 0, 508, 382)

    # bullets
    wave = []

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

        # endregion

        # region Computing
        # Wrapping
        player_x_without_wrap = player.position[0] - wrap.distance - initial_wrap.distance
        wrap.compute(delta)
        initial_wrap.compute(delta)
        player.position[0] = player_x_without_wrap + wrap.distance + initial_wrap.distance

        arena_rect.center = (wrap.distance + initial_wrap.distance, 0)

        # Check wave end
        if len(wave) == 0 and wrap.over:
            if not wave_launched:
                time_to_wave += delta
                if time_to_wave >= wave_wait_after_wrap:
                    wave_launched = True
                    time_to_wave = 0
                    engine.resources.play_sound(("wave_spawn",))
                    wave = level.waves[current_wave]

            else:
                time_to_next_wave += delta
                if time_to_next_wave >= wrap_delay_after_wave_end:
                    current_wave += 1
                    time_to_next_wave = 0
                    wave_launched = False

                    if wrap.distance > 79000:
                        return

                    Enemy.enemies_bullet_list.clear()
                    wrap.init_wrap()

        # Player update
        player.handle_key_pressed(key_pressed, delta)
        player.update(delta)
        player.constrain(arena_rect)
        if not player.alive:
            return

        # Enemies update
        for enemy in wave:
            enemy.update_surface(delta)
            enemy.update(delta, player)

        # Friendly bullets update
        for bullet in Player.player_bullet_list:
            bullet.update(delta)

            if not arena_rect.contains(bullet.rect):
                bullet.dead = True
                continue

            for enemy in wave:
                if bullet.check_collision(enemy):
                    bullet.dead = True
                    enemy.on_hit(bullet)

        # Remove dead friendly bullets
        length = len(Player.player_bullet_list)
        for i in range(len(Player.player_bullet_list)):
            index = length-1-i

            bullet = Player.player_bullet_list[index]
            if bullet.dead:
                bullet.remove_from_scene()
                Player.player_bullet_list.pop(index)

        # Enemy bullets update
        for bullet in Enemy.enemies_bullet_list:
            bullet.update(delta)

            if not arena_rect.contains(bullet.rect):
                bullet.dead = True
                continue

            if not player.invincible and player.rect.colliderect(bullet.rect):
                bullet.dead = True
                player.on_hit()

        # Remove dead enemy bullets
        length = len(Enemy.enemies_bullet_list)
        for i in range(len(Enemy.enemies_bullet_list)):
            index = length-1-i
            bullet = Enemy.enemies_bullet_list[index]
            if bullet.dead:
                bullet.remove_from_scene()
                Enemy.enemies_bullet_list.pop(index)

        # Remove dead enemies
        for enemy in wave:
            if enemy.dead:
                enemy.remove_from_scene()
                wave.remove(enemy)

        # Camera
        dx = (player.position[0] - wrap.distance - initial_wrap.distance) * player_camera_multiplier
        dy = player.position[1] * player_camera_multiplier
        camera.position = dx + wrap.distance + initial_wrap.distance, dy

        print(camera.position)

        # endregion

        # region Rendering
        screen.fill((13, 43, 69))
        camera.render_fixed_sprites(screen)
        camera.render_mobile_sprites(screen)

        screen.blit(engine.resources.images["menu"]["frame"], (100, 100))

        screen.crop_border()

        # pygame.draw.rect(screen.display, (255, 0, 0), (300, 124, 64, 64))

        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    _player = Player()
    _level = Level(1)
    game_level(_player, _level)
    pygame.quit()
