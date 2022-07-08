from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.options import options


def options_button_released_callback():
    resources.play_sound(("click",))
    options()


def options_button_hover_callback():
    resources.play_sound(("click",))


button_pos = 70, 90

options_sprite_up = Sprite(surface=resources.images["menu"]["options_up"],
                           position=button_pos)

options_sprite_down = Sprite(surface=resources.images["menu"]["options_down"],
                             position=button_pos)

options_button = Button(button_pos)

# Setting button callbacks
options_button.set_callback(options_button_released_callback, "released")
options_button.set_callback(options_button_hover_callback, "hover")

# Setting button rect / mask
options_button.set_rect_from_sprite(options_sprite_up, "hover")
options_button.set_rect_from_sprite(options_sprite_down, "released")

options_button_dict = {"button": options_button,
                       "sprite_up": options_sprite_up,
                       "sprite_down": options_sprite_down}
