import src.engine as engine

import pygame

from pygame.locals import *
from random import randint


def create_classic_sprites(_scene: engine.scene.Scene) -> None:

    sprite_nb = 1000
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000
    min_d, max_d = 0, 2

    for _ in range(sprite_nb):
        surface = engine.resources.images["cursors"][f"cursor_{randint(1, 6)}"]
        pos = randint(min_x, max_x), randint(min_y, max_y)
        depth = randint(min_d*10000, max_d*10000) / 10000
        raw_pos = randint(-200, 200), randint(-150, 150)

        new_sprite = engine.scene.Sprite(surface=surface, position=pos, depth=depth, raw_pos=raw_pos)

        _scene.add_fixed_sprite(new_sprite)


def create_shader_sprites(_scene: engine.scene.Scene) -> None:

    sprite_nb = 10
    min_x, max_x = -1000, 1000
    min_y, max_y = -1000, 1000
    min_d, max_d = 0, 2

    for _ in range(sprite_nb):
        shader = engine.shaders.GrayscaleShader
        pos = randint(min_x, max_x), randint(min_y, max_y)
        depth = randint(min_d*10000, max_d*10000) / 10000
        raw_pos = randint(-200, 200), randint(-150, 150)

        new_sprite = engine.scene.ShaderSprite(shader=shader,
                                               shader_value=(0.3, 0.59, 0.11),
                                               shader_size=(110, 110),
                                               pos=pos,
                                               depth=depth,
                                               raw_pos=raw_pos)

        _scene.add_fixed_sprite(new_sprite)
        _scene.add_fixed_sprite(new_sprite)


def main():
    loop_handler = engine.loop_handler
    resources = engine.resources
    screen = engine.screen

    # Scene
    camera_speed = 400
    scene, camera = engine.scene.create_scene_and_camera()
    create_classic_sprites(scene)
    create_shader_sprites(scene)
    background_sprite = engine.scene.Sprite(surface=resources.images["misc"]["frog"], position=(0, 0), depth=0)
    scene.add_fixed_sprite(background_sprite)
    scene.order()

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

        screen.fill((255, 0, 0))
        camera.render_fixed_sprites(screen)
        # resources.shaders[shaders_keys[shaders_index]].compute(screen, shaders_values[shaders_index])
        screen.crop_border()

        display_array = pygame.surfarray.pixels3d(screen.display)
        engine.shaders.CRT.compute(display_array, 0, 0, 0)
        del display_array

        pygame.display.flip()


if __name__ == '__main__':
    engine.init("../../assets")
    main()
    pygame.quit()
