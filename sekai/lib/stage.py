from math import cos, pi

from sonolus.script.interval import interp
from sonolus.script.runtime import is_multiplayer, is_play, is_replay, is_watch, time

from sekai.lib.custom_elements import (
    draw_life_number,
    draw_score_bar_number,
    draw_score_bar_raw_number,
    draw_score_number,
)
from sekai.lib.effect import SFX_DISTANCE, Effects
from sekai.lib.layout import (
    ScoreGaugeType,
    layout_background_cover,
    layout_custom_tag,
    layout_fallback_judge_line,
    layout_hidden_cover,
    layout_lane,
    layout_lane_by_edges,
    layout_life_bar,
    layout_life_gauge,
    layout_score_bar,
    layout_score_gauge,
    layout_score_rank,
    layout_score_rank_text,
    layout_sekai_stage,
    layout_stage_cover,
    layout_stage_cover_line,
)
from sekai.lib.options import Options
from sekai.lib.particle import ActiveParticles
from sekai.lib.skin import ActiveSkin, ScoreRankType


def draw_stage_and_accessories(
    z_stage_lane,
    z_stage_cover,
    z_stage,
    z_judgment_line,
    z_cover,
    z_cover_line,
    z_judgment,
    z_background_cover,
    z_layer_score,
    z_layer_score_glow,
    z_layer_score_bar,
    z_layer_score_bar_mask,
    z_layer_score_bar_rate,
    z_layer_background,
    ap,
    score,
    note_score,
    note_time,
    percentage,
    life=1000,
    last_time=1e8,
):
    draw_stage(z_stage_lane, z_stage_cover, z_stage, z_judgment_line)
    draw_stage_cover(z_cover, z_cover_line)
    draw_auto_play(z_judgment)
    draw_background_cover(z_background_cover)
    draw_dead(z_layer_background, life)
    draw_score_number(
        ap=ap,
        score=round(percentage, 4),
        z1=z_layer_score,
        z2=z_layer_score_glow,
    )
    draw_life_bar(life, z_layer_score, z_layer_score_glow, last_time)
    draw_score_bar(
        score,
        note_score,
        note_time,
        z_layer_score,
        z_layer_score_glow,
        z_layer_score_bar,
        z_layer_score_bar_mask,
        z_layer_score_bar_rate,
    )


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


def draw_dead(z_background, life):
    if life == 0:
        layout = layout_background_cover()
        ActiveSkin.background.draw(layout, z=z_background, a=0.3)


def draw_auto_play(z_judgment):
    if Options.custom_tag and is_watch() and not is_replay() and Options.hide_ui < 2:
        layout = layout_custom_tag()
        a = 0.8 * (cos(time() * pi) + 1) / 2
        ActiveSkin.auto_live.draw(layout, z=z_judgment, a=a)


def draw_life_bar(life, z_layer_score, z_layer_score_glow, last_time):
    if Options.hide_ui >= 2:
        return
    if not ActiveSkin.ui_number.available:
        return
    if not Options.custom_life_bar:
        return
    if not ActiveSkin.life.bar.available:
        return
    draw_life_number(
        life,
        z_layer_score_glow,
    )
    bar_layout = layout_life_bar()
    if is_multiplayer():
        ActiveSkin.life.bar.disable.draw(bar_layout, z=z_layer_score)
    elif last_time < time() and is_play():
        ActiveSkin.life.bar.skip.draw(bar_layout, z=z_layer_score)
    else:
        ActiveSkin.life.bar.pause.draw(bar_layout, z=z_layer_score)
    gauge_layout = layout_life_gauge(life)
    ActiveSkin.life.gauge.get_sprite(life).draw(gauge_layout, z_layer_score_glow)


def draw_score_bar(
    score,
    note_score,
    note_time,
    z_layer_score,
    z_layer_score_glow,
    z_layer_score_bar,
    z_layer_score_bar_mask,
    z_layer_score_bar_rate,
):
    if Options.hide_ui >= 2:
        return
    if not ActiveSkin.ui_number.available:
        return
    if not Options.custom_score_bar:
        return
    if not ActiveSkin.score.available:
        return
    draw_score_bar_number(
        score,
        z_layer_score_glow,
    )
    draw_score_bar_raw_number(number=note_score, z=z_layer_score_bar, time=time() - note_time)
    bar_layout = layout_score_bar()
    ActiveSkin.score.bar.draw(bar_layout, z=z_layer_score)
    ActiveSkin.score.panel.draw(bar_layout, z=z_layer_score_bar_rate)
    rank = get_score_rank(score)
    if score > 0:
        gauge = get_gauge_progress(score)
        gauge_mask = get_gauge_progress_mask(score)
        gauge_normal_layout = layout_score_gauge(score_type=ScoreGaugeType.NORMAL)
        ActiveSkin.score.gauge.normal.draw(gauge_normal_layout, z=z_layer_score_bar)
        if gauge_mask < 1:
            gauge_mask_layout = layout_score_gauge(gauge_mask, ScoreGaugeType.MASK)
            ActiveSkin.score.gauge.mask.draw(gauge_mask_layout, z=z_layer_score_bar_mask)
        gauge_mask_edge_layout = layout_score_gauge(gauge, score_type=ScoreGaugeType.EDGE)
        ActiveSkin.score.gauge.mask_edge.draw(gauge_mask_edge_layout, z=z_layer_score_bar_mask)
        score_rank_layout = layout_score_rank()
        ActiveSkin.score.rank.get_sprite(rank).draw(score_rank_layout, z=z_layer_score_glow)
    score_rank_text_layout = layout_score_rank_text()
    ActiveSkin.score.rank_text.get_sprite(rank).draw(score_rank_text_layout, z=z_layer_score_glow)


def get_gauge_progress(score):
    xp = (0, 3000, 300000, 520000, 740000, 1000000)
    fp = (0, 0.447, 0.6, 0.755, 0.908, 1.0)

    return interp(xp, fp, score)


def get_gauge_progress_mask(score):
    xp = (0, 3000, 300000, 520000, 740000, 960000)
    fp = (0, 0.447, 0.6, 0.755, 0.908, 1.0)

    return interp(xp, fp, score)


def get_score_rank(score):
    if score >= 740000:
        return ScoreRankType.S
    elif score >= 520000:
        return ScoreRankType.A
    elif score >= 300000:
        return ScoreRankType.B
    elif score >= 3000:
        return ScoreRankType.C
    else:
        return ScoreRankType.D


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
