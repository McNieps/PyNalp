import pygame
import sys


class LoopHandler:
    """A very, very clever class to handle anything related to game clock."""

    run = True

    max_fps = 60

    average_delta = 1 / max_fps
    delta = 0

    clock = pygame.time.Clock()

    @classmethod
    def is_running(cls):
        if cls.run:
            return True

        cls.run = True
        return False

    @classmethod
    def stop_loop(cls):
        cls.run = False

    @classmethod
    def stop_game(cls):
        pygame.quit()
        sys.exit()

    @classmethod
    def limit_and_get_delta(cls):
        cls.delta = cls.clock.tick(cls.max_fps) / 1000
        return cls.delta

    @classmethod
    def get_fps(cls):
        return cls.clock.get_fps()
