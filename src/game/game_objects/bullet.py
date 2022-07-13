from src.engine.scene import Sprite, Scene

import pygame


class Bullet:
    SCENE = Scene()
    enemy_bullet_list = []

    mask_dict: dict[pygame.Surface, pygame.mask.Mask] = {}

    def __init__(self, x, y, vx, vy, surf, damage):
        # Sprite
        self.sprite = Sprite(surf, (x, y))
        self.SCENE.add_mobile_sprite(self.sprite)
        self.surface = surf

        # Position and collision detection
        self.position = self.sprite.position
        self.velocity = [vx, vy]
        self.rect = self.surface.get_rect()
        if self.surface not in self.mask_dict:
            self.mask_dict[self.surface] = pygame.mask.from_surface(self.surface)
        self.mask = self.mask_dict[self.surface]
        self.rect.center = self.position

        # State
        self.dead = False
        self.damage = damage

    def update(self, delta):
        self.position[0] += self.velocity[0] * delta
        self.position[1] += self.velocity[1] * delta
        self.rect.center = self.position

    def remove_from_scene(self):
        self.SCENE.mobile_sprites.remove(self.sprite)

    def check_collision(self, entity):
        offset = entity.rect[0] - self.rect[0], entity.rect[1] - self.rect[1]
        return self.mask.overlap(entity.mask, offset)
