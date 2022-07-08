from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources, loop_handler


def quit_button_callback():
    loop_handler.stop_game()


button_pos = 70, 190

quit_sprite = Sprite(surface=resources.images["menu"]["quit_button"],
                     position=button_pos)

quit_button = Button(button_pos)
quit_button.set_callback(quit_button_callback, "released")
quit_button.set_rect_from_sprite(quit_sprite, "released")
