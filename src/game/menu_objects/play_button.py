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

play_sprite = Sprite(surface=resources.images["menu"]["play_button"],
                     position=button_pos)

play_button = Button(button_pos)

# Setting button callbacks
play_button.set_callback(play_button_released_callback, "released")
play_button.set_callback(play_button_hover_callback, "hover")

# Setting button rect / mask
play_button.set_rect_from_sprite(play_sprite, ["released", "hover"])
