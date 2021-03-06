if __name__ == '__main__':
    import os
    os.chdir("../")

from src.game.states.sector_selection import sector_selection
from src.game.states.game_level import game_level
from src.game.states.defeat import defeat
from src.game.states.victory import victory

from src.game.menu_objects.map.galaxy import Galaxy

from src.game.game_objects.player import Player


def game():
    galaxy = Galaxy()
    player = Player()

    game_level(player, galaxy.current_sector.level)

    for i in range(5):
        if player.alive:
            sector_selection(galaxy, player)
            player.reset()
            game_level(player, galaxy.current_sector.level)

    if player.alive:
        victory()

    else:
        defeat()


if __name__ == '__main__':
    game()
