from src.engine.gui import Button

import pygame


class GUI:
    def __init__(self):
        # Mouse states
        self._mouse_pos = (0, 0)
        self._mouse_just_pressed = False
        self._mouse_just_released = False
        self._mouse_button_down = False

        # Things like buttons, ...
        self.elements = set()

    def add_element(self,
                    element: Button) -> None:
        """
        Add a button to the GUI.

        Args:
            element: The element to add.
        """

        self.elements.add(element)

    def mouse_pressed(self):
        self._mouse_just_pressed = True
        self._mouse_button_down = True

    def mouse_released(self):
        self._mouse_just_released = True
        self._mouse_button_down = False

    def update(self) -> None:
        """
        Update all GUI elements
        """

        mouse_pos = pygame.mouse.get_pos()

        # cheap hovering
        if mouse_pos == self._mouse_pos:
            for element in self.elements:
                element.mouse_cheap_hover()

        # costly hovering
        else:
            for element in self.elements:
                element.mouse_hover(mouse_pos)

        # pressed
        if self._mouse_just_pressed:
            for element in self.elements:
                element.mouse_pressed(mouse_pos)

        # released
        if self._mouse_just_released:
            for element in self.elements:
                element.mouse_released(mouse_pos)

        self._mouse_pos = mouse_pos
        self._mouse_just_pressed = False
        self._mouse_just_released = False
