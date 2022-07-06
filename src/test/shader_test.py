import src.engine as engine

import pygame

from pygame.locals import *
from random import randint
from time import time


def create_classic_sprites(_scene: engine.scene.Scene,
                           _resources: engine.handlers.ResourceHandler) -> None:

    sprite_nb = 1000
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000
    min_d, max_d = 0, 2

    for _ in range(sprite_nb):
        surface = _resources.images["cursors"][f"cursor_{randint(1, 6)}"]
        pos = randint(min_x, max_x), randint(min_y, max_y)
        depth = randint(min_d*10000, max_d*10000) / 10000
        raw_pos = randint(-200, 200), randint(-150, 150)

        new_sprite = engine.scene.Sprite(surface=surface,
                                         pos=pos,
                                         depth=depth,
                                         raw_pos=raw_pos)

        _scene.add_fixed_sprite(new_sprite)


def create_shader_sprites(_scene: engine.scene.Scene,
                          _resources: engine.handlers.ResourceHandler) -> None:

    sprite_nb = 10
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000
    min_d, max_d = 0, 2

    for _ in range(sprite_nb):
        shader = _resources.shaders["grayscale"]
        pos = randint(min_x, max_x), randint(min_y, max_y)
        depth = randint(min_d*10000, max_d*10000) / 10000
        raw_pos = randint(-200, 200), randint(-150, 150)

        new_sprite = engine.scene.ShaderSprite(shader=shader,
                                               shader_value=(0.3, 0.59, 0.11),
                                               shader_size=(110, 110),
                                               pos=pos,
                                               depth=depth,
                                               raw_pos=raw_pos)

        print(new_sprite.screen_rect)

        _scene.add_fixed_sprite(new_sprite)
        _scene.add_fixed_sprite(new_sprite)


def main():
    resources = engine.resources
    screen = engine.screen

    loop_handler = engine.handlers.LoopHandler()

    # Scene
    camera_speed = 400
    scene, camera = engine.scene.create_scene_and_camera()
    create_classic_sprites(scene, resources)
    create_shader_sprites(scene, resources)
    background_sprite = engine.scene.Sprite(surface=resources.images["frog"],
                                            pos=(0, 0),
                                            depth=0)
    scene.add_fixed_sprite(background_sprite)
    scene.order()

    # Shaders
    shaders_keys = list(resources.shaders.keys())
    shaders_index = 0
    shaders_values = [3, 5, ((10, 10), (0, 0), (-10, -10)), 5]
    shaders_strength = 5
    t = time()
    resources.shaders["blackhole"].pre_gen_shader_map([500], [i/10 for i in range(100)], verbose=True)
    print(time()-t)

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()
        pygame.display.set_caption(f"FPS: {loop_handler.get_fps()}")

        # Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_game()
                elif event.key == K_UP:
                    shaders_index = (shaders_index + 1) % len(shaders_keys)
                elif event.key == K_DOWN:
                    shaders_index = (shaders_index - 1) % len(shaders_keys)
                elif event.key == K_LEFT:
                    shaders_strength -= 1
                elif event.key == K_RIGHT:
                    shaders_strength += 1

        key_pressed = pygame.key.get_pressed()
        speed = camera_speed * delta
        if key_pressed[K_d]:
            camera.x += speed
        if key_pressed[K_q]:
            camera.x -= speed
        if key_pressed[K_s]:
            camera.y += speed
        if key_pressed[K_z]:
            camera.y -= speed
        if key_pressed[K_LEFT]:
            shaders_strength -= 10 * delta
        if key_pressed[K_RIGHT]:
            shaders_strength += 10 * delta

        screen.fill((255, 0, 0))
        camera.render_fixed_sprites(screen)
        # resources.shaders[shaders_keys[shaders_index]].compute(screen, shaders_values[shaders_index])
        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()
