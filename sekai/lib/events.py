from sekai.lib.layer import LAYER_BACKGROUND_COVER
from sekai.lib.layout import (
    layout_fever_cover_left,
    layout_fever_cover_right,
)
from sekai.lib.skin import Skin


def draw_fever_side_cover():
    layout1 = layout_fever_cover_left()
    layout2 = layout_fever_cover_right()
    Skin.background.draw(layout1, LAYER_BACKGROUND_COVER, a=0.8)
    Skin.background.draw(layout2, LAYER_BACKGROUND_COVER, a=0.8)
