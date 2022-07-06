import pygame


class LoopHandler:
    MAX_FPS = 60
    AVG_DELTA = 1 / MAX_FPS
    STOP = False

    def __init__(self,
                 max_fps=None):
        """A very, very clever class to handle anything related to game clock."""

        self.clock = pygame.time.Clock()
        self.run = not self.STOP

        self.max_fps = max_fps
        if max_fps is None:
            self.max_fps = self.MAX_FPS

        self.delta = 0  # 1 / self.MAX_FPS

    def is_running(self):
        return self.run

    def stop_loop(self):
        self.run = False

    def stop_game(self):
        self.run = False
        self.STOP = True

    def limit_and_get_delta(self):
        self.delta = self.clock.tick(self.max_fps) / 1000
        return self.delta

    def get_fps(self):
        return self.clock.get_fps()
