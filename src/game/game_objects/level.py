import src.engine as engine

from src.game.game_objects.enemies.kami import Kami
from src.game.game_objects.enemies.beholder import Beholder

import random


class Level:
    MAX_PLAYER_INDUCED_OFFSET = (40, 30)

    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        self.number_of_waves = 5

        # level
        self.waves = []

        # scene
        self.stars = []
        self.number_of_stars = 1_000
        self.length = 100_000

        # self.generate_level()
        self._generate_scene()

    def generate_level(self):
        for i in range(self.number_of_waves):
            wave_list = []
            wave_pos = self.length / self.number_of_waves * (i + 1)

            match self.difficulty:
                case 1:
                    for _ in range(random.randint(2, 4)):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                case 2:
                    for _ in range(random.randint(4, 6)):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                case 3:
                    for _ in range(random.randint(4, 6)):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                    for _ in range(1):
                        wave_list.append(Beholder(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                case 4:
                    for _ in range(random.randint(5, 7)):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                    for _ in range(2):
                        wave_list.append(Beholder(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                case 5:
                    for _ in range(random.randint(5, 7)):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                    for _ in range(3):
                        wave_list.append(Beholder(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                case 6:
                    for _ in range(6):
                        wave_list.append(Kami(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

                    for _ in range(4):
                        wave_list.append(Beholder(wave_pos + random.randint(100, 150), random.randint(-180, 180)))

            self.waves.append(wave_list)

    def _generate_scene(self):
        min_x = int(-self.MAX_PLAYER_INDUCED_OFFSET[0]/2)
        max_x = int(self.MAX_PLAYER_INDUCED_OFFSET[1]/2 + self.length)
        min_y = int(-self.MAX_PLAYER_INDUCED_OFFSET[1]/2)
        max_y = int(self.MAX_PLAYER_INDUCED_OFFSET[1]/2)

        for _ in range(self.number_of_stars):
            star_color = random.randint(1, 3)
            star_type = random.randint(1, 4)
            star_surf = engine.resources.images["environment"][f"star_{star_type}_{star_color}"]

            star_pos = random.randint(min_x, max_x), random.randint(min_y, max_y)
            star_depth = abs(random.gauss(0, 1))
            star_screen_offset = random.randint(-200, 200), random.randint(-150, 150)

            star_sprite = engine.scene.Sprite(star_surf, star_pos, star_depth, star_screen_offset)
            self.stars.append(star_sprite)

        for i in range(1, self.number_of_waves + 1):
            x = self.length / self.number_of_waves * i

            planet_screen_offset = random.randint(-200, 200), random.randint(-150, 150)

            planet_surf = engine.resources.images["environment"][f"planet_{random.randint(1, 4)}"]
            planet_sprite = engine.scene.Sprite(planet_surf, (x, 0), 0.5, planet_screen_offset)
            self.stars.append(planet_sprite)
