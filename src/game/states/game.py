if __name__ == '__main__':
    import os
    os.chdir("../")

from src.game.states.sector_selection import sector_selection
from src.game.game_objects.map.galaxy import Galaxy


def game():
    galaxy = Galaxy()
    sector_selection(galaxy)
    # player = Player()
    # galaxy_map = Galaxy(seed=seed)

    # current_sector = galaxy_map.get_current_sector()
    # win = game_level(player, current_sector)

    # while win and not current_sector.final:
    #     sector = sector_selection(galaxy_map, current_sector)
    #     win = game_level(player, current_sector)

    # if not win:
    #     game_over_screen()
    # else:
    #     win_screen()

    pass


if __name__ == '__main__':
    game()
