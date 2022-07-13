import src.engine as engine

from src.engine.scene import Sprite, Scene

import pygame


class Enemy:
    SCENE = Scene()
    enemies_bullet_list = []

    mask_dict: dict[pygame.Surface, pygame.mask.Mask] = {}

    def __init__(self, x, y, surfs: list[pygame.Surface], frequency: float):
        self.sprite = Sprite(surfs[0], (x, y))
        self.SCENE.add_mobile_sprite(self.sprite)

        # Position and collision detection
        self.position = self.sprite.position
        self.velocity = [0, 0]
        self.rect = surfs[0].get_rect()
        self.rect.center = self.position
        if surfs[0] not in self.mask_dict:
            self.mask_dict[surfs[0]] = pygame.mask.from_surface(surfs[0])
        self.mask = self.mask_dict[surfs[0]]
        self.damping = 0.5

        # Animation
        self.surfaces = surfs
        self.anim_time = 0
        self.anim_count = len(surfs)
        self.spf = 1/frequency   # second per frame

        # Other
        self.dead = False
        self.health = 50

    def update_surface(self, delta):
        self.anim_time = (self.anim_time + delta / self.spf) % self.anim_count
        surf_to_set = self.surfaces[int(self.anim_time)]
        self.sprite.surface = surf_to_set

        if surf_to_set not in self.mask_dict:
            self.mask_dict[surf_to_set] = pygame.mask.from_surface(surf_to_set)
        self.mask = self.mask_dict[surf_to_set]

    def update(self, delta, player):
        self.velocity[0] *= self.damping ** delta
        self.velocity[1] *= self.damping ** delta
        self.position[0] += self.velocity[0] * delta
        self.position[1] += self.velocity[1] * delta
        self.rect.center = self.position

    def on_hit(self, bullet):
        engine.resources.play_sound(("enemy_hit",))

        self.health -= bullet.damage

        if self.health <= 0:
            self.on_death()

    def on_death(self):
        self.dead = True

    def remove_from_scene(self):
        self.SCENE.mobile_sprites.remove(self.sprite)
