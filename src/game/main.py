"""
Hello dear pygamer.
"""


from src.game.states.menu import menu

import pygame


def main():
    pygame.mixer.music.load("assets/sounds/music.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    menu()
    pygame.quit()


if __name__ == '__main__':
    main()
