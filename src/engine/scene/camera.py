from src.engine.scene.scene import Scene
from src.engine.screen import Screen
from src.engine.scene.typing import SpriteStyle

import pygame


class Camera:
    _SCREEN_SIZE = (800, 600)
    _BLIT_OFFSET = (800 / 2, 600 / 2)
    _SHADER_MAX_SIZE = 0

    def __init__(self,
                 scene: Scene,
                 position: tuple[float, float] = (0, 0)) -> None:

        # TODO compute adjusted_sprite_position with vector and numba for better performances
        self.position = position
        self.rect = pygame.Rect((0, 0), self._SCREEN_SIZE)
        self.rect.center = position

        self.scene = scene

        self.linked_sprite = None

    # region position methods
    @property
    def x(self) -> float:
        return self.position[0]

    @x.setter
    def x(self, value) -> None:
        self.position = value, self.position[1]
        self.rect.center = self.position

    @property
    def y(self) -> float:
        return self.position[1]

    @y.setter
    def y(self, value) -> None:
        self.position = self.position[0], value
        self.rect.center = self.position
    # endregion

    def get_active_cluster(self) -> tuple[int, int]:
        """Return the cluster coordinates to render"""
        return (int((self.x + self._SCREEN_SIZE[0] / 2) // self._SCREEN_SIZE[0]),
                int((self.y + self._SCREEN_SIZE[1] / 2) // self._SCREEN_SIZE[1]))

    def draw_active_cluster(self,
                            surface: pygame.Surface,
                            color: tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Draw one rect representing the current cluster
        TODO: render text showing current cluster pos
        """

        active_cluster = self.get_active_cluster()

        rect = pygame.Rect(active_cluster[0] * self._SCREEN_SIZE[0] - self.x + self._SHADER_MAX_SIZE,
                           active_cluster[1] * self._SCREEN_SIZE[1] - self.y + self._SHADER_MAX_SIZE,
                           self._SCREEN_SIZE[0],
                           self._SCREEN_SIZE[1])

        pygame.draw.rect(surface, color, rect, 2)

    def _adjusted_sprite_position(self,
                                  sprite: SpriteStyle) -> tuple[int, int]:
        """This method can be used to calculate the position of the sprite on the screen relative to the camera"""

        dx = (sprite.position[0] - self.position[0]) * sprite.depth + self._BLIT_OFFSET[0]
        dy = (sprite.position[1] - self.position[1]) * sprite.depth + self._BLIT_OFFSET[1]

        return int(dx), int(dy)

    def draw_sprite(self,
                    sprite: SpriteStyle,
                    surface: pygame.Surface) -> None:
        """This method can be used to draw a sprite into the screen"""

        # return screen.blit(sprite.surface, self.adjusted_sprite_position(sprite))
        sprite.draw(surface, self._adjusted_sprite_position(sprite))

    def render_fixed_sprites(self,
                             screen: Screen,
                             zone: list[int] = None) -> None:
        """
        Method used to draw fixed sprite on the screen.

        Args:
            screen: The screen object (engine object)
            zone: 2>foreground, 1> background, 0> quasistatic, -1> weirdground
        """

        if zone is None:
            zone = [-1, 0, 1, 2]

        zone.sort()
        active_cluster = self.get_active_cluster()

        # Draw weirdground then static then background
        for depth in [-1, 0, 1, 2]:
            if depth not in zone:
                continue

            if depth == 0:
                sprites = self.scene.depth_planes[0]

            elif active_cluster not in self.scene.depth_planes[depth]:
                continue

            else:
                sprites = self.scene.depth_planes[depth][active_cluster]

            for sprite in sprites:
                self.draw_sprite(sprite, screen)
                # sprite.draw(screen.surface, self.adjusted_sprite_position(sprite))

    def render_mobile_sprites(self,
                              screen: Screen):
        """
        Method used to render mobile sprites on the screen.

        Args:
            screen: The screen object (engine object)
        """

        for sprite in self.scene.mobile_sprites:

            # Check collision with screen
            if sprite.screen_rect.colliderect(sprite.rect):
                self.draw_sprite(sprite, screen)
