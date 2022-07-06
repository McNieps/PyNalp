import src.engine as engine
import src.test.utils as utils

import pygame
import pymunk
import pymunk.pygame_util

from pygame.locals import *
from math import degrees


# Main loop function
def main():
    resources = engine.resources
    screen = engine.screen

    loop_handler = engine.handlers.LoopHandler()
    scene, camera = engine.scene.create_scene_and_camera()
    utils.create_classic_sprites(scene, resources)

    space = pymunk.Space()
    space.gravity = (0, 1000)
    space.sleep_time_threshold = 5
    space.idle_speed_threshold = 20
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    chti_pos = (40, 100)
    chti_sprite = engine.scene.AdvancedSprite(resources.images["chti"], chti_pos)
    scene.add_mobile_sprite(chti_sprite)
    chti_phy = engine.physics.Body(chti_pos)

    chti_phy.shape_poly_from_surface(resources.images["chti"], radius=-1, scale=0.5, concave=True, tolerance=2)
    # chti_phy.shape_rect((50, 50))
    # chti_phy.shape_circle(30)

    chti_phy.set_shapes_attributes(density=1, elasticity=1.05, friction=2)

    chti_phy.add_to_space(space)
    # chti_phy.remove_from_space()

    chti_phy.set_velocity((500, 0))
    floor = pymunk.Segment(body=space.static_body, a=(0, 300), b=(400, 300), radius=5)
    ceil = pymunk.Segment(body=space.static_body, a=(0, 0), b=(400, 0), radius=5)
    wall_l = pymunk.Segment(body=space.static_body, a=(0, 0), b=(0, 300), radius=5)
    wall_r = pymunk.Segment(body=space.static_body, a=(400, 0), b=(400, 300), radius=5)

    for seg in [floor, ceil, wall_l, wall_r]:
        seg.elasticity = 1
        seg.friction = 0.7
        space.add(seg)

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()
        pygame.display.set_caption(f"FPS: {loop_handler.get_fps()}")

        # region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loop_handler.stop_game()
                elif event.key == K_RETURN:
                    if chti_phy.is_sleeping:
                        print("ACTIVATE")
                        chti_phy.activate()
                    else:
                        print("SLEEP")
                        chti_phy.sleep()

        utils.move_camera(camera, delta)   # Move camera with z q s d keys (french layout)

        # endregion

        # region Computing
        space.step(delta)
        chti_sprite.x, chti_sprite.y = chti_phy.position[0], chti_phy.position[1]
        chti_sprite.angle = -degrees(chti_phy.angle)
        camera.x, camera.y = chti_sprite.x, chti_sprite.y

        # endregion

        # region Rendering
        screen.fill((0, 0, 0))

        camera.render_fixed_sprites(screen, zone=[-1, 0, 1])
        draw_options.transform = pymunk.Transform.translation(-camera.x + 300, -camera.y + 250)
        space.debug_draw(draw_options)
        camera.render_mobile_sprites(screen)
        camera.render_fixed_sprites(screen, zone=[2])

        # camera.draw_active_cluster(screen, (255, 255, 255))
        screen.crop_border()

        pygame.display.flip()

        # endregion


if __name__ == '__main__':
    main()
    pygame.quit()
