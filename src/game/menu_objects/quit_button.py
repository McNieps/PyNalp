from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources, loop_handler


def quit_button_released_callback():
    resources.play_sound(("click",))
    loop_handler.stop_game()


def quit_button_hover_callback():
    resources.play_sound(("click",))


button_pos = 70, 190

quit_sprite = Sprite(surface=resources.images["menu"]["quit_button"],
                     position=button_pos)

quit_button = Button(button_pos)

# Setting button callbacks
quit_button.set_callback(quit_button_released_callback, "released")
quit_button.set_callback(quit_button_hover_callback, "hover")

# Setting button rect / mask
quit_button.set_rect_from_sprite(quit_sprite, ["released", "hover"])
