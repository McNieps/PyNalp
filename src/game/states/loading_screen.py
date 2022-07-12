import src.engine as engine

import pygame
import threading

from pygame.locals import *
from typing import Callable
from sys import exit


def loading_screen(function_to_run: Callable, args: tuple):
    thread = threading.Thread(target=function_to_run, args=args)
    thread.start()

    counter = 0
    counter_fps = 5
    counter_frames = 5

    while thread.is_alive():
        delta = engine.loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        engine.screen.fill((255, 255, 255))

        counter = (counter + counter_fps * delta) % counter_frames

        engine.screen.fill(0)
        engine.screen.blit(engine.resources.images["loading_screen"]["loading_screen_frame"], (100, 100))
        engine.screen.blit(engine.resources.images["loading_screen"][f"anim_{int(counter+1)}"], (434, 328))

        engine.screen.crop_border()
        pygame.display.flip()
