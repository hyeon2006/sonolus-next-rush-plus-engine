from sonolus.script.interval import lerp, unlerp_clamped

from sekai.lib.layout import (
    LANE_B,
    LANE_T,
    layout_fever_cover_left,
    layout_fever_cover_right,
    layout_fever_gauge_left,
    layout_fever_gauge_right,
    layout_sekai_stage,
)
from sekai.lib.skin import ActiveSkin


def draw_fever_side_cover(z: float, time: float):
    if not ActiveSkin.background.is_available:
        return
    layout1 = layout_fever_cover_left()
    layout2 = layout_fever_cover_right()
    a = unlerp_clamped(0, 0.25, time) * 0.75
    ActiveSkin.background.draw(layout1, z, a=a)
    ActiveSkin.background.draw(layout2, z, a=a)


def draw_fever_side_bar(z: float, time: float):
    if not ActiveSkin.sekai_stage_fever.is_available:
        return
    layout = layout_sekai_stage()
    a = unlerp_clamped(0, 0.25, time)
    ActiveSkin.sekai_stage_fever.draw(layout, z, a=a)


def draw_fever_gauge(z: float, percentage: float):
    if not ActiveSkin.sekai_fever_gauge.available:
        return
    t = lerp(LANE_B, LANE_T, percentage)
    layout1 = layout_fever_gauge_left(t)
    layout2 = layout_fever_gauge_right(t)
    ActiveSkin.sekai_fever_gauge.get_sprite(percentage).draw(layout1, z, a=0.55)
    ActiveSkin.sekai_fever_gauge.get_sprite(percentage).draw(layout2, z, a=0.55)
