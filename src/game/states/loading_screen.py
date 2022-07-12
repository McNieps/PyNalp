import src.engine as engine

import pygame
import threading

from pygame.locals import *
from typing import Callable
from sys import exit


def loading_screen(function_to_run: Callable, args: tuple):
    thread = threading.Thread(target=function_to_run, args=args)
    thread.start()

    frog_angle = 0
    frog_center = 450, 350

    while thread.is_alive():
        delta = engine.loop_handler.limit_and_get_delta()
        print(engine.loop_handler.get_fps())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        engine.screen.fill((255, 255, 255))

        frog_angle += 180 * delta
        frog = pygame.transform.rotate(engine.resources.images["environment"]["galaxy_1"], frog_angle)
        frog_rect = frog.get_rect()
        frog_rect.center = frog_center
        engine.screen.blit(frog, frog_rect)

        engine.screen.crop_border()
        pygame.display.flip()
