import src.engine as engine

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
    MOVE_CONTROLS = move_controls_azerty
    ACTION_CONTROLS = action_controls

    def __init__(self):
        # State
        self.alive = True
        self.sensor_broken = False
        self.motor_broken = False
        self.aux_broken = False

        # Position and velocity
        self._position = [0, 0]
        self._velocity = [0, 0]
        self._damping = 0.99

        # Sprite
        self.sprite = engine.scene.AdvancedSprite([engine.resources.images["player"]["90L"]], (0, 0))
        self.sprite.position = self._position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position[0] = value[0]
        self._position[1] = value[1]

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

            self._velocity[0] += vec.x
            self._velocity[1] += vec.y

        self._velocity[0] *= self._damping ** delta
        self._velocity[1] *= self._damping ** delta

        self._position[0] += self._velocity[0]
        self._position[1] += self._velocity[1]
