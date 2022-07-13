from src.game.main import main

import pygame


if __name__ == '__main__':
    pygame.mixer.music.load("assets/sounds/music.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

    main()
    pygame.quit()
