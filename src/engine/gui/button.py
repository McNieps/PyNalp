from src.engine.scene.sprites import Sprite
from src.engine.gui.typing import ValidMouseAction
from src.engine.typing import SpriteStyle

import pygame

from typing import Callable, Union


class Button:
    _DISPLAY_RECT = (0, 0, 400, 300)

    def __init__(self,
                 position: tuple[int, int] = (0, 0),
                 one_time_hover: bool = True,
                 pressed_when_released: bool = False) -> None:
        """
        A button.

        Args:
            position: The center of the button relative to the screen.
            one_time_hover: If set to True:
                The hover callback function will only be called once until the mouse leave the button. Default to True.
            pressed_when_released: If set to True:
                The released callback function will only be called if the button has been pressed. Default to False.
        """

        self.position = position
        self.hovered = False
        self.pressed = False

        self._one_time_hover = one_time_hover
        self._pressed_when_released = pressed_when_released

        self._hover_cb = None
        self._hover_body = pygame.Rect(0, 0, 0, 0)

        self._pressed_cb = None
        self._pressed_body = pygame.Rect(0, 0, 0, 0)

        self._released_cb = None
        self._released_body = pygame.Rect(0, 0, 0, 0)

    def set_rect_from_sprite(self,
                             sprite: SpriteStyle,
                             action_type: ValidMouseAction) -> pygame.Rect:
        """
        Method used to define rect for the action_type.

        Args:
            sprite:
            action_type: "hover", "pressed", "released"

        Returns:
            The defined rect
        """

        rect = pygame.Rect(0, 0, *sprite.rect.size)
        rect.center = self.position

        match action_type:
            case "hover":
                self._hover_body = rect
            case "pressed":
                self._pressed_body = rect
            case "released":
                self._released_body = rect
            case _:
                raise ValueError(f'action type "{action_type}" is not valid.')

        return rect

    def set_mask_from_sprite(self,
                             sprite: Sprite,
                             action_type: ValidMouseAction) -> pygame.mask.Mask:
        """
        Method used to define mask for the action_type.

        Args:
            sprite:
            action_type: "hover", "pressed", "released"

        Returns:
            The defined mask
        """

        mask = pygame.mask.from_surface(sprite.surface)
        match action_type:
            case "hover":
                self._hover_body = mask
            case "pressed":
                self._pressed_body = mask
            case "released":
                self._released_body = mask
            case _:
                raise ValueError(f'action type "{action_type}" is not valid.')

        return mask

    def set_body(self,
                 body: Union[pygame.Rect, pygame.mask.Mask],
                 action_type: ValidMouseAction) -> None:
        """
        Set collision shape for the given action_type.

        Args:
            body: A rect or a mask. Will be centered around the button position.
            action_type: "hover", "pressed", "released"
        """

        match action_type:
            case "hover":
                self._hover_body = body
            case "pressed":
                self._pressed_body = body
            case "released":
                self._released_body = body
            case _:
                raise ValueError(f'action type "{action_type}" is not valid.')

    def set_callback(self,
                     callback: Callable,
                     action_type: ValidMouseAction) -> None:
        """
        Set a callback for the given action_type.

        Args:
            callback: A callable without any arguments.
            action_type: "hover", "pressed", "released".
        """

        match action_type:
            case "hover":
                self._hover_cb = callback
            case "pressed":
                self._pressed_cb = callback
            case "released":
                self._released_cb = callback
            case _:
                raise ValueError(f'action type "{action_type}" is not valid.')

    def mouse_pressed(self,
                      mouse_pos: tuple[int, int]) -> None:
        """
        Method to call when the mouse button just went down.

        Args:
            mouse_pos: The coordinates of the mouse when the mouse button has been pressed.
        """

        if self._check_mouse_collision(mouse_pos=mouse_pos, action_type="pressed"):
            self.pressed = True
            self._pressed_cb()

    def mouse_released(self,
                       mouse_pos: tuple[int, int]) -> None:
        """
        Method to call when the mouse button just went up.

        Args:
            mouse_pos: The coordinates of the mouse when the mouse button has been released.
        """

        collision = self._check_mouse_collision(mouse_pos=mouse_pos, action_type="released")

        if not collision:
            self.pressed = False
            return

        if not self._pressed_when_released:
            self._released_cb()
            self.pressed = False
            return

        if self.pressed:
            self._released_cb()

        self.pressed = False
        return

    def mouse_hover(self,
                    mouse_pos: tuple[int, int]) -> None:
        """
        Method to call all the time if the mouse move.

        Args:
            mouse_pos: The coordinates of the mouse.
        """

        collision = self._check_mouse_collision(mouse_pos=mouse_pos, action_type="hover")

        if collision:
            if self._one_time_hover:
                if self.hovered:
                    return
                self.hovered = True
                self._hover_cb()
                return
            else:
                self._hover_cb()
                self.hovered = True
                return

        self.hovered = False

    def mouse_cheap_hover(self):
        """Method to call all the time if the mouse don't move."""

        if self._one_time_hover:
            return

        if self.hovered:
            self._hover_cb()

    def _check_mouse_collision(self,
                               mouse_pos: tuple[int, int],
                               action_type: ValidMouseAction) -> bool:
        """
        Method to check if the button is actually actuated.

        Args:
            mouse_pos: The mouse position.
            action_type: "hover", "pressed", "released".

        Returns:
            A bool indicating if the button is actuated or not.
        """

        match action_type:
            case "hover":
                collision_body = self._hover_body
            case "pressed":
                collision_body = self._pressed_body
            case "released":
                collision_body = self._released_body
            case _:
                raise ValueError(f'action type "{action_type}" is not valid.')

        # collision_body is pygame.Rect
        if isinstance(collision_body, pygame.Rect):
            return collision_body.collidepoint(*mouse_pos)

        # collision_body is pygame.mask.Mask
        elif isinstance(collision_body, pygame.mask.Mask):
            size = collision_body.get_size()
            sprite_rect = pygame.Rect((0, 0), size)
            sprite_rect.center = self.position

            if sprite_rect.collidepoint(*mouse_pos):
                relative_mouse_pos = (mouse_pos[0]-sprite_rect[0],
                                      mouse_pos[1]-sprite_rect[1])
                return bool(collision_body.get_at(relative_mouse_pos))

        return False
