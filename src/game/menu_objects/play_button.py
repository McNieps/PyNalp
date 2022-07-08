from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.game import game


def play_button_released_callback():
    resources.play_sound(("click",))
    game()


def play_button_hover_callback():
    resources.play_sound(("click",))


button_pos = 70, 40

play_sprite_up = Sprite(surface=resources.images["menu"]["play_up"],
                        position=button_pos)

play_sprite_down = Sprite(surface=resources.images["menu"]["play_down"],
                          position=button_pos)

play_button = Button(button_pos)

# Setting button callbacks
play_button.set_callback(play_button_released_callback, "released")
play_button.set_callback(play_button_hover_callback, "hover")

# Setting button rect / mask
play_button.set_rect_from_sprite(play_sprite_up, "hover")
play_button.set_rect_from_sprite(play_sprite_up, "released")

play_button_dict = {"button": play_button,
                    "sprite_up": play_sprite_up,
                    "sprite_down": play_sprite_down}
