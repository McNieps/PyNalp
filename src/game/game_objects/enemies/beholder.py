import src.engine as engine

from src.game.game_objects.enemies.enemy import Enemy
from src.game.game_objects.bullet import Bullet

import pygame
import math
import random


class Beholder(Enemy):
    def __init__(self, x, y):
        surfs = [engine.resources.images["enemies"][f"beholder_{i}"] for i in range(1, 9)]

        super().__init__(x, y, surfs, 9)

        self.speed = 30
        self.min_dist = 100
        self.max_dist = 120
        self.health = 50

        # Shoot
        self.over = False
        self.firing_duration = 5
        self.firing_since = 0
        self.firing_cooldown = 4
        self.number_of_bullets = 100
        self.seconds_per_bullet = self.firing_duration / self.number_of_bullets
        self.leftover = 0.0
        self.bullet_speed = 150

    def update(self, delta, player):
        dx = player.position[0] - self.position[0]
        dy = player.position[1] - self.position[1]

        vec = pygame.math.Vector2(dx, dy)

        dist = vec.magnitude()
        vec.normalize_ip()

        if dist < self.min_dist:
            vec *= -self.speed * delta
            self.position[0] += vec[0]
            self.position[1] += vec[1]

        elif dist > self.max_dist:
            vec *= self.speed * delta
            self.position[0] += vec[0]
            self.position[1] += vec[1]

        Enemy.update(self, delta, player)
        self.shoot(delta)

    def shoot(self, delta):
        if not self.over:
            self.leftover += delta

            for _ in range(int(self.leftover // self.seconds_per_bullet)):
                x, y = self.position
                angle = random.uniform(0, math.tau)
                vx, vy = math.cos(angle) * self.bullet_speed, math.sin(angle) * self.bullet_speed
                self.enemies_bullet_list.append(Bullet(x, y, vx, vy,
                                                       engine.resources.images["bullet"]["enemy_bullet"], 1))

            self.leftover = self.leftover % self.seconds_per_bullet

            self.firing_since += delta
            if self.firing_since > self.firing_duration:
                self.over = True
                self.firing_since = 0
                self.leftover = 0

        else:
            self.firing_since += delta
            if self.firing_since >= self.firing_cooldown:
                self.firing_since = 0
                self.over = False

    def on_death(self):
        engine.resources.play_sound(("beholder_death",))
        Enemy.on_death(self)
