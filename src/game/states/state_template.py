import src.engine as engine

import pygame

from pygame.locals import *


def template():
    loop_handler = engine.loop_handler
    resources = engine.resources
    screen = engine.screen

    # Main loop
    while loop_handler.is_running():
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            if event.type == QUIT:
                loop_handler.stop_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                loop_handler.stop_loop()

        # region Rendering
        screen.fill((0, 0, 0))

        screen.crop_border()
        pygame.display.flip()


if __name__ == '__main__':
    engine.init("../../../assets")
    template()
    pygame.quit()
