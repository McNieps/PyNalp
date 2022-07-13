import src.engine as engine

from src.game.game_objects.enemies.enemy import Enemy
from src.game.game_objects.bullet import Bullet

import pygame
import math


class Kami(Enemy):
    def __init__(self, x, y, vx=0, vy=0):

        surfs = [engine.resources.images["enemies"]["kami_1"]]
        super().__init__(x, y, surfs, 1)

        self.velocity[0] = vx
        self.velocity[1] = vy
        self.speed = 80

        self.health = 15
        self.number_of_bullet = 20
        self.bullet_speed = 66

    def update(self, delta, player):
        dx = player.position[0] - self.position[0]
        dy = player.position[1] - self.position[1]

        if self.mask.overlap(player.mask, (dx, dy)):
            self.on_death()
            return

        vec = pygame.math.Vector2(dx, dy)
        vec.normalize_ip()
        vec *= self.speed * delta

        self.position[0] += vec[0]
        self.position[1] += vec[1]

        Enemy.update(self, delta, player)

    def on_hit(self, bullet):
        Enemy.on_hit(self, bullet)
        self.velocity[0] += bullet.velocity[0] / 75
        self.velocity[1] += bullet.velocity[1] / 75

    def on_death(self):
        engine.resources.play_sound(("kami_death",))
        for i in range(self.number_of_bullet):
            angle = i * math.tau / self.number_of_bullet
            x, y = self.position
            vx, vy = math.cos(angle) * self.bullet_speed, math.sin(angle) * self.bullet_speed

            Enemy.enemies_bullet_list.append(Bullet(x, y, vx, vy, engine.resources.images["bullet"]["enemy_bullet"], 1))

        Enemy.on_death(self)
