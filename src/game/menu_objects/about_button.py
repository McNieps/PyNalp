from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.about import about


def about_button_released_callback():
    resources.play_sound(("click",))
    about()


def about_button_hover_callback():
    resources.play_sound(("click",))


button_pos = 70, 140

about_sprite_up = Sprite(surface=resources.images["menu"]["about_up"],
                         position=button_pos)

about_sprite_down = Sprite(surface=resources.images["menu"]["about_down"],
                           position=button_pos)

about_button = Button(button_pos)

# Setting button callbacks
about_button.set_callback(about_button_released_callback, "released")
about_button.set_callback(about_button_hover_callback, "hover")

# Setting button rect / mask
about_button.set_rect_from_sprite(about_sprite_up, "hover")
about_button.set_rect_from_sprite(about_sprite_down, "released")

about_button_dict = {"button": about_button,
                     "sprite_up": about_sprite_up,
                     "sprite_down": about_sprite_down}
