import src.engine as engine

from src.game.game_objects.bullet import Bullet

import pygame

from pygame.locals import *


# for arrows (works with qwerty, azerty and others)
move_controls_arrow_key = {"up": K_UP,
                           "down": K_DOWN,
                           "left": K_LEFT,
                           "right": K_RIGHT}

# for qwerty keyboards (wasd)
move_controls_qwerty = {"up": K_w,
                        "down": K_s,
                        "left": K_a,
                        "right": K_d}

# for azerty keyboards (zqsd)
move_controls_azerty = {"up": K_z,
                        "down": K_s,
                        "left": K_q,
                        "right": K_d}

action_controls = {"shoot": K_RETURN}


class Player:
    MOVE_CONTROLS = move_controls_qwerty
    ACTION_CONTROLS = action_controls

    player_bullet_list = []

    def __init__(self):
        # Sprite
        self._surface = engine.resources.images["player"]["chti_saucer"]

        # State
        self.alive = True
        self.sensor_broken = False
        self.motor_broken = False
        self.aux_broken = False

        # Position and velocity
        self.starting_x = 0
        self._position = [self.starting_x, 0]
        self._velocity = [0, 0]
        self._speed = 175
        self.rect = self._surface.get_rect()
        self.mask = pygame.mask.from_surface(self._surface)

        # Weapon
        self.rate_of_fire = 10
        self.fire_period = 1 / self.rate_of_fire
        self.can_shoot = True
        self.time_to_shoot = 0
        self.damage = 1

        # Shield
        self.shield_on = True
        self.shield_refill_time = 5
        self.shield_current_time = 0

        # Invulnerability frames
        self.inv_duration = 0.25
        self.invincible = False
        self.inv_current = 0

        # If motor broken
        self._damping = 0.2

        # Sprite
        self.sprite = engine.scene.AdvancedSprite([self._surface], (0, 0))
        self.sprite.position = self._position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position[0] = value[0]
        self._position[1] = value[1]

    def constrain(self, arena_rect: pygame.Rect):
        self.rect.center = self.position
        changed_x = False
        changed_y = False

        if self.rect.left < arena_rect.left:
            changed_x = True
            self.rect.left = arena_rect.left
            self._velocity[0] *= -0.8

        elif self.rect.right > arena_rect.right:
            changed_x = True
            self.rect.right = arena_rect.right
            self._velocity[0] *= -0.8

        if self.rect.top < arena_rect.top:
            changed_y = True
            self.rect.top = arena_rect.top
            self._velocity[1] *= -0.8

        elif self.rect.bottom > arena_rect.bottom:
            changed_y = True
            self.rect.bottom = arena_rect.bottom
            self._velocity[1] *= -0.8

        if changed_x:
            self.position[0] = self.rect.centerx
        if changed_y:
            self.position[1] = self.rect.centery

    def reset(self):
        self.position = (self.starting_x, 0)
        self._velocity = [0, 0]
        self.shield_on = True
        self.aux_broken = False
        self.motor_broken = False
        self.sensor_broken = False

    def reload(self, delta):
        if self.time_to_shoot > 0:
            self.time_to_shoot -= delta

    def clean_reload(self):
        if self.time_to_shoot < 0:
            self.time_to_shoot = 0

    def shoot(self):
        while self.time_to_shoot <= 0:
            self.time_to_shoot += self.fire_period

            bullet = Bullet(self.position[0] + 5,
                            self.position[1],
                            1000,
                            0,
                            engine.resources.images["bullet"]["player_bullet"],
                            self.damage)

            engine.resources.play_sound(("shoot",))

            self.player_bullet_list.append(bullet)

    def update_shield(self, delta):
        if not self.shield_on:
            self.shield_current_time += delta

            if self.shield_current_time > self.shield_refill_time:
                self.shield_current_time = 0
                self.shield_on = True

    def update(self, delta):
        if not self.shield_on:
            self.shield_current_time += delta
            if self.shield_current_time >= self.shield_refill_time:
                self.shield_current_time = 0
                self.shield_on = True
                engine.resources.play_sound(("shield", "up"))

        if self.invincible:
            self.inv_current += delta
            if self.inv_current > self.inv_duration:
                self.inv_current = 0
                self.invincible = False

    def on_hit(self):
        if self.shield_on:
            self.shield_on = False
            engine.resources.play_sound(("shield", "down"))
            self.invincible = True
        else:
            self.alive = False

    def handle_key_pressed(self, key_pressed: list[int], delta: float):
        vec = pygame.Vector2(0, 0)
        if key_pressed[self.MOVE_CONTROLS["up"]]:
            vec.y -= 1
        if key_pressed[self.MOVE_CONTROLS["down"]]:
            vec.y += 1
        if key_pressed[self.MOVE_CONTROLS["left"]]:
            vec.x -= 1
        if key_pressed[self.MOVE_CONTROLS["right"]]:
            vec.x += 1

        magnitude_sq = vec.magnitude_squared()

        if magnitude_sq:
            vec.normalize_ip()
            vec *= delta

        # max_speed = -max_speed + speed) * damping

        if self.motor_broken:
            self._velocity[0] += vec.x * self._speed
            self._velocity[1] += vec.y * self._speed

        else:
            self._position[0] += vec.x * self._speed
            self._position[1] += vec.y * self._speed

        self._velocity[0] *= self._damping ** delta
        self._velocity[1] *= self._damping ** delta

        self._position[0] += self._velocity[0] * delta
        self._position[1] += self._velocity[1] * delta

        self.reload(delta)
        if key_pressed[self.ACTION_CONTROLS["shoot"]]:
            self.shoot()
        else:
            self.clean_reload()
