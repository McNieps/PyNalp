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

about_sprite = Sprite(surface=resources.images["menu"]["about_button"],
                      position=button_pos)

about_button = Button(button_pos)

# Setting button callbacks
about_button.set_callback(about_button_released_callback, "released")
about_button.set_callback(about_button_hover_callback, "hover")

# Setting button rect / mask
about_button.set_rect_from_sprite(about_sprite, ["released", "hover"])
