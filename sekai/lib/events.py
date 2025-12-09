from sonolus.script.interval import lerp, unlerp_clamped

from sekai.lib.layout import (
    LANE_B,
    LANE_T,
    layout_fever_cover_left,
    layout_fever_cover_right,
    layout_fever_gauge_left,
    layout_fever_gauge_right,
    layout_fever_text,
    layout_lane,
    layout_sekai_stage,
    perspective_rect,
)
from sekai.lib.options import Options
from sekai.lib.particle import ActiveParticles
from sekai.lib.skin import ActiveSkin


def draw_fever_side_cover(z: float, time: float):
    if not ActiveSkin.background.is_available:
        return
    if Options.record_mode:
        return
    layout1 = layout_fever_cover_left()
    layout2 = layout_fever_cover_right()
    a = unlerp_clamped(0, 0.25, time) * 0.75
    ActiveSkin.background.draw(layout1, z, a=a)
    ActiveSkin.background.draw(layout2, z, a=a)


def draw_fever_side_bar(z: float, time: float):
    if not ActiveSkin.sekai_stage_fever.is_available:
        return
    if Options.record_mode:
        return
    layout = layout_sekai_stage()
    a = unlerp_clamped(0, 0.25, time)
    ActiveSkin.sekai_stage_fever.draw(layout, z, a=a)


def draw_fever_gauge(z: float, percentage: float):
    if not ActiveSkin.sekai_fever_gauge.available:
        return
    if Options.record_mode:
        return
    t = lerp(LANE_B, LANE_T, percentage)
    layout1 = layout_fever_gauge_left(t)
    layout2 = layout_fever_gauge_right(t)
    ActiveSkin.sekai_fever_gauge.get_sprite(percentage).draw(layout1, z, a=0.55)
    ActiveSkin.sekai_fever_gauge.get_sprite(percentage).draw(layout2, z, a=0.55)


def spawn_fever_start_particle(cant_super_fever: bool):
    if Options.record_mode:
        return
    if cant_super_fever:
        layout_text = layout_fever_text()
        layout_lane1 = layout_lane(-6, 1)
        layout_lane2 = layout_lane(6, 1)
        ActiveParticles.fever_start_text.spawn(layout_text, 1, False)
        if Options.fever_effect == 0:
            ActiveParticles.fever_start_lane.spawn(layout_lane1, 1, False)
            ActiveParticles.fever_start_lane.spawn(layout_lane2, 1, False)
    else:
        layout_text = layout_fever_text()
        layout_lane1 = layout_lane(-6, 1)
        layout_lane2 = layout_lane(6, 1)
        mid = (LANE_T + LANE_B) / 2
        layout_effect1 = perspective_rect(l=-6 - 0.5, r=-6 + 0.5, t=mid - 0.050075, b=mid + 0.050075)
        layout_effect2 = perspective_rect(l=6 - 0.5, r=6 + 0.5, t=mid - 0.050075, b=mid + 0.050075)
        ActiveParticles.super_fever_start_text.spawn(layout_text, 1, False)
        if Options.fever_effect == 0:
            ActiveParticles.super_fever_start_lane.spawn(layout_lane1, 1, False)
            ActiveParticles.super_fever_start_lane.spawn(layout_lane2, 1, False)
            ActiveParticles.super_fever_start_effect.spawn(layout_effect1, 1, False)
            ActiveParticles.super_fever_start_effect.spawn(layout_effect2, 1, False)


def spawn_fever_chance_particle():
    if Options.record_mode:
        return
    layout_text = layout_fever_text()
    layout_lane1 = layout_lane(-6, 0.5)
    layout_lane2 = layout_lane(6, 0.5)
    ActiveParticles.fever_chance_text.spawn(layout_text, 1, False)
    if Options.fever_effect == 0:
        ActiveParticles.fever_chance_lane.spawn(layout_lane1, 1, False)
        ActiveParticles.fever_chance_lane.spawn(layout_lane2, 1, False)
