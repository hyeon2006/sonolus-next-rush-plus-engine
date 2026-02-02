from sekai.lib.effect import SFX_DISTANCE, Effects
from sekai.lib.layer import LAYER_COVER, LAYER_JUDGMENT_LINE, LAYER_STAGE, get_z
from sekai.lib.layout import (
    layout_fallback_judge_line,
    layout_hidden_cover,
    layout_lane,
    layout_lane_by_edges,
    layout_sekai_stage,
    layout_stage_cover,
)
from sekai.lib.options import Options
from sekai.lib.particle import ActiveParticles
from sekai.lib.skin import ActiveSkin


def draw_stage_and_accessories():
    draw_stage()
    draw_stage_cover()


def draw_stage():
    if not Options.show_lane:
        return
    if ActiveSkin.sekai_stage.is_available:
        draw_sekai_stage()
    else:
        draw_fallback_stage()


def draw_sekai_stage():
    layout = layout_sekai_stage()
    ActiveSkin.sekai_stage.draw(layout, z=get_z(LAYER_STAGE))


def draw_fallback_stage():
    layout = layout_lane_by_edges(-6.5, -6)
    ActiveSkin.stage_left_border.draw(layout, z=get_z(LAYER_STAGE))
    layout = layout_lane_by_edges(6, 6.5)
    ActiveSkin.stage_right_border.draw(layout, z=get_z(LAYER_STAGE))

    for lane in (-5, -3, -1, 1, 3, 5):
        layout = layout_lane(lane, 1)
        ActiveSkin.lane.draw(layout, z=get_z(LAYER_STAGE))

    layout = layout_fallback_judge_line()
    ActiveSkin.judgment_line.draw(layout, z=get_z(LAYER_JUDGMENT_LINE))


def draw_stage_cover():
    if Options.stage_cover > 0:
        layout = layout_stage_cover()
        ActiveSkin.cover.draw(layout, z=get_z(LAYER_COVER), a=1)
    if Options.hidden > 0:
        layout = layout_hidden_cover()
        ActiveSkin.cover.draw(layout, z=get_z(LAYER_COVER), a=1)


def play_lane_hit_effects(lane: float):
    play_lane_sfx(lane)
    play_lane_particle(lane)


def play_lane_sfx(lane: float):
    if Options.sfx_enabled:
        Effects.stage.play(SFX_DISTANCE)


def schedule_lane_sfx(lane: float, target_time: float):
    if Options.sfx_enabled:
        Effects.stage.schedule(target_time, SFX_DISTANCE)


def play_lane_particle(lane: float):
    if Options.lane_effect_enabled:
        layout = layout_lane(lane, 0.5)
        ActiveParticles.lane.spawn(layout, duration=0.3 / Options.effect_animation_speed)
