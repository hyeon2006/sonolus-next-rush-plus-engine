from math import cos, pi

from sonolus.script.runtime import is_replay, is_watch, time

from sekai.lib.effect import SFX_DISTANCE, Effects
from sekai.lib.layout import (
    layout_background_cover,
    layout_custom_tag,
    layout_fallback_judge_line,
    layout_hidden_cover,
    layout_lane,
    layout_lane_by_edges,
    layout_sekai_stage,
    layout_stage_cover,
    layout_stage_cover_line,
)
from sekai.lib.options import Options
from sekai.lib.particle import ActiveParticles
from sekai.lib.skin import ActiveSkin


def draw_stage_and_accessories(
    z_stage_lane, z_stage_cover, z_stage, z_judgment_line, z_cover, z_cover_line, z_judgment, z_background_cover
):
    draw_stage(z_stage_lane, z_stage_cover, z_stage, z_judgment_line)
    draw_stage_cover(z_cover, z_cover_line)
    draw_auto_play(z_judgment)
    draw_background_cover(z_background_cover)


def draw_stage(z_stage_lane, z_stage_cover, z_stage, z_judgment_line):
    if not Options.show_lane:
        return
    if ActiveSkin.sekai_stage_lane.is_available and ActiveSkin.sekai_stage_cover.is_available:
        draw_sekai_divided_stage(z_stage_lane, z_stage_cover)
    elif ActiveSkin.sekai_stage.is_available:
        draw_sekai_stage(z_stage)
    else:
        draw_fallback_stage(z_stage, z_judgment_line)


def draw_sekai_stage(z_stage):
    layout = layout_sekai_stage()
    ActiveSkin.sekai_stage.draw(layout, z=z_stage)


def draw_sekai_divided_stage(z_stage_lane, z_stage_cover):
    layout = layout_sekai_stage()
    ActiveSkin.sekai_stage_lane.draw(layout, z=z_stage_lane)
    ActiveSkin.sekai_stage_cover.draw(layout, z=z_stage_cover, a=Options.lane_alpha)


def draw_fallback_stage(z_stage, z_judgment_line):
    layout = layout_lane_by_edges(-6.5, -6)
    ActiveSkin.stage_left_border.draw(layout, z=z_stage)
    layout = layout_lane_by_edges(6, 6.5)
    ActiveSkin.stage_right_border.draw(layout, z=z_stage)

    for lane in (-5, -3, -1, 1, 3, 5):
        layout = layout_lane(lane, 1)
        ActiveSkin.lane.draw(layout, z=z_stage)

    layout = layout_fallback_judge_line()
    ActiveSkin.judgment_line.draw(layout, z=z_judgment_line)


def draw_stage_cover(z_cover, z_cover_line):
    if Options.stage_cover > 0:
        layout = layout_stage_cover()
        layout2 = layout_stage_cover_line()
        ActiveSkin.cover.draw(layout, z=z_cover, a=0.9)
        ActiveSkin.guide_neutral.draw(layout2, z=z_cover_line, a=0.75)
    if Options.hidden > 0:
        layout = layout_hidden_cover()
        ActiveSkin.cover.draw(layout, z=z_cover, a=1)


def draw_background_cover(z_background_cover):
    if Options.background_alpha != 1:
        layout = layout_background_cover()
        ActiveSkin.background.draw(layout, z=z_background_cover, a=1 - Options.background_alpha)


def draw_auto_play(z_judgment):
    if Options.custom_tag and is_watch() and not is_replay() and not Options.record_mode:
        layout = layout_custom_tag()
        a = 0.8 * (cos(time() * pi) + 1) / 2
        ActiveSkin.auto_live.draw(layout, z=z_judgment, a=a)


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
        ActiveParticles.lane.spawn(layout, duration=0.3)
