from src.engine.scene.sprites import *
from src.engine.typing import sprite_style

import pygame

from math import floor
from typing import Union


class Scene:
    __slots__ = ("_foreground_clusters",
                 "_background_clusters",
                 "_quasistatic_sprites",
                 "_weirdground_clusters",
                 "sprites",
                 "mobile_sprites",
                 "_index_names",
                 "depth_planes")

    _GLOBAL_DEPTH_THRESHOLD = 0.001
    _SCREEN_SIZE = (400, 300)
    _SHADERS_ENABLED = False

    def __init__(self) -> None:
        """
        2D Scene, composed of multiple cluster, containing multiple sprites each. Only one cluster can be visible at a
        time.
        """

        self.sprites = []
        self.mobile_sprites = []
        self._foreground_clusters = {}
        self._background_clusters = {}
        self._quasistatic_sprites = []
        self._weirdground_clusters = {}

        self._index_names = ["quasistatic sprites",
                             "background sprites",
                             "foreground sprites",
                             "weirdground sprites"]

        self.depth_planes = [self._quasistatic_sprites,
                             self._background_clusters,
                             self._foreground_clusters,
                             self._weirdground_clusters]

    def _get_cluster_coord(self,
                           pos: tuple[int, int]) -> tuple[int, int]:
        """
        Method used to get the active cluster to render
        """

        # return floor(pos[0] * self._INV_SCREEN_SIZE[0]), floor(pos[1] * self._INV_SCREEN_SIZE[1])
        return pos[0] // self._SCREEN_SIZE[0], pos[1] // self._SCREEN_SIZE[1]

    def _get_sprite_clusters(self,
                             sprite: sprite_style,
                             rect: Union[pygame.Rect, None]) -> list[tuple[int, int]]:
        """
        Return clusters where the sprite is visible. Assume that the sprite will move!

        Args:
            sprite: The sprite to that will be added to the scene
            rect: The zone of action of the sprite, AROUND ITS INITIAL POS
        """

        sprite_clusters = []
        sprite_depth = abs(sprite.depth)

        if sprite_depth < self._GLOBAL_DEPTH_THRESHOLD:
            return sprite_clusters

        sprite_rect = pygame.Rect(0, 0, *sprite.rect.size)
        sprite_rect.center = sprite.position

        i_offset = (self._SCREEN_SIZE[0] / 2 + sprite_rect.width / 2) / sprite_depth
        j_offset = (self._SCREEN_SIZE[1] / 2 + sprite_rect.height / 2) / sprite_depth

        min_cluster_i = -i_offset + sprite_rect.centerx
        max_cluster_i = i_offset + sprite_rect.centerx
        min_cluster_j = -j_offset + sprite_rect.centery
        max_cluster_j = j_offset + sprite_rect.centery

        # If the sprite is moving
        # Note: weirdground sprite zoning may behave badly, fix it maybe?
        if rect:
            min_cluster_i -= rect.left / sprite_depth
            max_cluster_i += rect.right / sprite_depth
            min_cluster_j -= rect.top / sprite_depth
            max_cluster_j += rect.bottom / sprite_depth

        # round cluster coords
        min_cluster_i = floor(min_cluster_i / self._SCREEN_SIZE[0] - 0.5)
        max_cluster_i = floor(max_cluster_i / self._SCREEN_SIZE[0] + 1.5)
        min_cluster_j = floor(min_cluster_j / self._SCREEN_SIZE[1] - 0.5)
        max_cluster_j = floor(max_cluster_j / self._SCREEN_SIZE[1] + 1.5)

        for j in range(min_cluster_j, max_cluster_j):
            for i in range(min_cluster_i, max_cluster_i):
                sprite_clusters.append((i, j))

        return sprite_clusters

    def add_fixed_sprite(self,
                         sprite: sprite_style) -> None:
        """
        Add a fixed sprite to the scene.

        Args:
            sprite: The sprite to that will be added to the scene.
        """

        self.add_zoned_sprite(sprite, pygame.Rect(0, 0, 0, 0))

    def add_zoned_sprite(self,
                         sprite: sprite_style,
                         zone: pygame.Rect) -> None:
        """
        Add a zoned sprite to the scene.

        Args:
            sprite: The sprite to that will be added to the scene.
            zone: The zone of action of the sprite, AROUND ITS INITIAL POS.
        """

        # Prevent sprite to be added to space if sprite is ShaderSprite and shaders are disabled
        if not self._SHADERS_ENABLED and isinstance(sprite, ShaderSprite):
            return

        # Check sprite clusters
        sprite_clusters = self._get_sprite_clusters(sprite, zone)

        # If quasistatic
        if not sprite_clusters:
            self._quasistatic_sprites.append(sprite)
            return

        # If weirdground
        if sprite.depth < 0:
            for cluster in sprite_clusters:
                if cluster not in self._weirdground_clusters:
                    self._weirdground_clusters[cluster] = []
                self._weirdground_clusters[cluster].append(sprite)
            return

        # If background
        if sprite.depth <= 1:
            for cluster in sprite_clusters:
                if cluster not in self._background_clusters:
                    self._background_clusters[cluster] = []
                self._background_clusters[cluster].append(sprite)
            return

        # If foreground
        for cluster in sprite_clusters:
            if cluster not in self._foreground_clusters:
                self._foreground_clusters[cluster] = []

            self._foreground_clusters[cluster].append(sprite)

    def add_mobile_sprite(self,
                          sprite: sprite_style) -> None:
        """
        Add a mobile sprite to the scene.
        A mobile sprite is not subject to clusterization and will only be drawn if it's visible.
        Mobile sprites will be drawn ON TOP OF fixed/zoned sprites. IDK how to do it another way...

        Args:
            sprite: The sprite to that will be added to the scene.
        """

        self.mobile_sprites.append(sprite)

    def order(self,
              planes_to_order: list[int] = None,
              clusters_to_order: list[tuple[int, int]] = None) -> None:
        """
        Used to order different zones (foreground, background, ...) in order to draw them from the farthest to the
        nearest.

        Args:
            planes_to_order: 2>foreground, 1> background, 0> quasistatic, -1> weirdground.
            clusters_to_order: the clusters coordinates to order.
        """

        if planes_to_order is None:
            planes_to_order = [-1, 0, 1, 2]

        planes_to_order.sort()

        for depth in planes_to_order:
            if depth == 0:
                self.depth_planes[0].sort()
                continue

            plane = self.depth_planes[depth]

            if clusters_to_order is None:
                iterator = plane.keys()
            else:
                iterator = clusters_to_order

            for cluster in iterator:
                if cluster in plane:
                    plane[cluster].sort()
