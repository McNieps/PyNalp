from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.game import game


def options_button_callback():
    print("Options")


button_pos = 70, 90

options_sprite = Sprite(surface=resources.images["menu"]["options_button"],
                        position=button_pos)

options_button = Button(button_pos)
options_button.set_callback(options_button_callback, "released")
options_button.set_rect_from_sprite(options_sprite, "released")
