from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.game import game


def about_button_callback():
    print("About")


button_pos = 70, 140

about_sprite = Sprite(surface=resources.images["menu"]["about_button"],
                      position=button_pos)

about_button = Button(button_pos)
about_button.set_callback(about_button_callback, "released")
about_button.set_rect_from_sprite(about_sprite, "released")
