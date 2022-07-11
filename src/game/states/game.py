if __name__ == '__main__':
    import os
    os.chdir("../")

from src.game.states.sector_selection import sector_selection
from src.game.states.game_level import game_level
from src.game.menu_objects.map.galaxy import Galaxy


def game():
    galaxy = Galaxy()
    # player = Player()

    for i in range(5):
        sector_selection(galaxy)

    # win = game_level(player, current_sector)

    # while win and not current_sector.final:
    #     sector_selection(galaxy_map)
    #     win = game_level(player, galaxy.current_sector.level)

    # if not win:
    #     game_over_screen()
    # else:
    #     win_screen()

    pass


if __name__ == '__main__':
    game()
