from src.engine.gui import Button
from src.engine.scene import Sprite
from src.engine import resources

from src.game.states.about import about


def hover_callback():
    resources.play_sound(("click",))


def released_callback():
    resources.play_sound(("click",))
    about()


def pressed_callback():
    resources.play_sound(("click",))


button_pos = 70, 140

sprite_up = Sprite(surface=resources.images["menu"]["about_up"],
                   position=button_pos)

sprite_down = Sprite(surface=resources.images["menu"]["about_down"],
                     position=button_pos)

button = Button(button_pos)

# Setting button callbacks
button.set_callback(hover_callback, "hover")
button.set_callback(pressed_callback, "pressed")
button.set_callback(released_callback, "released")

# Setting button rect / mask
button.set_rect_from_sprite(sprite_up, "hover")
button.set_rect_from_sprite(sprite_up, "pressed")
button.set_rect_from_sprite(sprite_down, "released")

about_button_dict = {"button": button,
                     "sprite_up": sprite_up,
                     "sprite_down": sprite_down}
