import pygame


class Screen(pygame.Surface):
    SHADERS_ENABLED = False
    SHADERS_MAX_SIZE = 0

    def __init__(self, display: pygame.Surface) -> None:
        """
        Custom object that is used to easily blit on a bigger surface than the default display surface.
        Shaders can be used and reveal details that were not visible on the default surface (e.g. black holes).

        """

        self.display = display
        self.display_size = self.display.get_size()
        self.display_rect = pygame.Rect(self.SHADERS_MAX_SIZE, self.SHADERS_MAX_SIZE, *self.display_size)

        size = tuple([self.display_size[i] + 2 * self.SHADERS_MAX_SIZE for i in range(2)])
        super().__init__(size=size)
        self.size = self.get_size()
        self.rect = self.get_rect()

    def crop_border(self) -> None:
        """
        Blit the frame-buffer into the display.
        Average time: 0.06 ms / call for 400*300 surface
        """

        self.display.blit(self.subsurface(self.display_rect), (0, 0))

    def show_all(self):
        """
        Resize the frame-buffer then blit it to the display. Deformations will occur.
        Used to see what's happening behind the scene.
        """

        pygame.transform.scale(self, self.display_size, self.display)
