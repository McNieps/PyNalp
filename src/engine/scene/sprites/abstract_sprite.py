import pygame


class AbstractSprite:
    __slots__ = ("position", "depth", "rect", "half_size")

    _SCREEN_RECT = pygame.Rect(0, 0, 400, 300)
    _DISPLAY_RECT = pygame.Rect(0, 0, 400, 300)
    _GLOBAL_DEPTH_THRESHOLD = 0.001

    def __init__(self,
                 sprite_size: tuple[int, int],
                 pos: tuple[float, float],
                 depth: float = 1,
                 raw_pos: tuple[float, float] = None) -> None:

        self.position = list(pos)
        if raw_pos is not None and abs(depth) > self._GLOBAL_DEPTH_THRESHOLD:
            self.position[0] += raw_pos[0]/depth
            self.position[1] += raw_pos[1]/depth

        self.depth = depth

        self.rect = pygame.Rect(0, 0, *sprite_size)

        self.half_size = sprite_size[0]/2, sprite_size[1]/2

    # region position methods
    @property
    def x(self) -> float:
        return self.position[0]

    @x.setter
    def x(self, value) -> None:
        self.position[0] = value

    @property
    def y(self) -> float:
        return self.position[1]

    @y.setter
    def y(self, value) -> None:
        self.position[1] = value

    @property
    def screen_rect(self):
        return self._SCREEN_RECT

    def __gt__(self, other):
        return self.depth > other.depth

    def __lt__(self, other):
        return other.depth > self.depth
    # endregion
