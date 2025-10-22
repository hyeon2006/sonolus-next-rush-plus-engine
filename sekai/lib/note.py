from enum import IntEnum, auto
from typing import assert_never, cast

from sonolus.script.archetype import ArchetypeLife, EntityRef, PlayArchetype, WatchArchetype, get_archetype_by_name
from sonolus.script.bucket import Bucket, Judgment, JudgmentWindow
from sonolus.script.easing import ease_in_cubic
from sonolus.script.effect import Effect
from sonolus.script.interval import Interval, lerp, remap_clamped
from sonolus.script.runtime import is_tutorial, is_watch, level_score, time
from sonolus.script.sprite import Sprite

from sekai.lib import archetype_names
from sekai.lib.buckets import (
    EMPTY_JUDGMENT_WINDOW,
    FLICK_CRITICAL_WINDOW,
    FLICK_NORMAL_WINDOW,
    FLICK_NORMAL_WINDOW_BAD,
    SLIDE_END_CRITICAL_WINDOW,
    SLIDE_END_FLICK_CRITICAL_WINDOW,
    SLIDE_END_FLICK_NORMAL_WINDOW,
    SLIDE_END_NORMAL_WINDOW,
    SLIDE_END_TRACE_CRITICAL_WINDOW,
    SLIDE_END_TRACE_NORMAL_WINDOW,
    TAP_CRITICAL_WINDOW,
    TAP_CRITICAL_WINDOW_BAD,
    TAP_NORMAL_WINDOW,
    TAP_NORMAL_WINDOW_BAD,
    TRACE_CRITICAL_WINDOW,
    TRACE_FLICK_CRITICAL_WINDOW,
    TRACE_FLICK_NORMAL_WINDOW,
    TRACE_NORMAL_WINDOW,
    Buckets,
)
from sekai.lib.ease import EaseType, ease
from sekai.lib.effect import EMPTY_EFFECT, SFX_DISTANCE, Effects, first_available_effect
from sekai.lib.layer import (
    LAYER_NOTE_ARROW,
    LAYER_NOTE_BODY,
    LAYER_NOTE_FLICK_BODY,
    LAYER_NOTE_SLIM_BODY,
    LAYER_NOTE_TICK,
    get_z,
)
from sekai.lib.layout import (
    FlickDirection,
    Layout,
    approach,
    get_alpha,
    iter_slot_lanes,
    layout_circular_effect,
    layout_flick_arrow,
    layout_flick_arrow_fallback,
    layout_lane,
    layout_linear_effect,
    layout_regular_note_body,
    layout_regular_note_body_fallback,
    layout_rotated_linear_effect,
    layout_slim_note_body,
    layout_slim_note_body_fallback,
    layout_tick,
    layout_tick_effect,
    preempt_time,
    progress_to,
)
from sekai.lib.options import Options
from sekai.lib.particle import (
    NoteParticleSet,
    critical_flick_note_particles,
    critical_note_particles,
    critical_slide_note_particles,
    critical_tick_particles,
    critical_trace_flick_note_particles,
    critical_trace_note_particles,
    damage_note_particles,
    empty_note_particles,
    first_available_particle,
    flick_note_particles,
    normal_note_particles,
    normal_tick_particles,
    slide_note_particles,
    trace_flick_note_particles,
    trace_note_particles,
)
from sekai.lib.skin import (
    ArrowSprites,
    BodySprites,
    Skin,
    TickSprites,
    critical_arrow_sprites,
    critical_note_body_sprites,
    critical_tick_sprites,
    critical_trace_note_body_sprites,
    critical_trace_tick_sprites,
    damage_note_body_sprites,
    flick_note_body_sprites,
    normal_arrow_sprites,
    normal_note_body_sprites,
    normal_tick_sprites,
    normal_trace_note_body_sprites,
    normal_trace_tick_sprites,
    slide_note_body_sprites,
    trace_flick_note_body_sprites,
    trace_flick_tick_sprites,
    trace_slide_note_body_sprites,
)
from sekai.lib.slot_effect import (
    SLOT_EFFECT_DURATION,
    SLOT_GLOW_EFFECT_DURATION,
    draw_slot_effect,
    draw_slot_glow_effect,
)
from sekai.lib.timescale import group_scaled_time_to_first_time, group_scaled_time_to_first_time_2


class NoteKind(IntEnum):
    NORM_TAP = auto()
    CRIT_TAP = auto()

    NORM_FLICK = auto()
    CRIT_FLICK = auto()

    NORM_TRACE = auto()
    CRIT_TRACE = auto()

    NORM_TRACE_FLICK = auto()
    CRIT_TRACE_FLICK = auto()

    NORM_RELEASE = auto()
    CRIT_RELEASE = auto()

    NORM_HEAD_TAP = auto()
    CRIT_HEAD_TAP = auto()

    NORM_HEAD_FLICK = auto()
    CRIT_HEAD_FLICK = auto()

    NORM_HEAD_TRACE = auto()
    CRIT_HEAD_TRACE = auto()

    NORM_HEAD_TRACE_FLICK = auto()
    CRIT_HEAD_TRACE_FLICK = auto()

    NORM_HEAD_RELEASE = auto()
    CRIT_HEAD_RELEASE = auto()

    NORM_TAIL_TAP = auto()
    CRIT_TAIL_TAP = auto()

    NORM_TAIL_FLICK = auto()
    CRIT_TAIL_FLICK = auto()

    NORM_TAIL_TRACE = auto()
    CRIT_TAIL_TRACE = auto()

    NORM_TAIL_TRACE_FLICK = auto()
    CRIT_TAIL_TRACE_FLICK = auto()

    NORM_TAIL_RELEASE = auto()
    CRIT_TAIL_RELEASE = auto()

    NORM_TICK = auto()
    CRIT_TICK = auto()
    HIDE_TICK = auto()

    DAMAGE = auto()

    ANCHOR = auto()


def init_score():
    level_score().update(
        perfect_multiplier=1.0,
        great_multiplier=0.7,
        good_multiplier=0.5,
        consecutive_great_multiplier=0.01,
        consecutive_great_step=100,
        consecutive_great_cap=1000,
    )


def init_note_life(archetype: type[PlayArchetype | WatchArchetype]):
    life = get_note_life(cast(NoteKind, archetype.key))
    archetype.life.update(
        perfect_increment=life.perfect_increment,
        great_increment=life.great_increment,
        good_increment=life.good_increment,
        miss_increment=life.miss_increment,
    )


def map_note_kind(kind: NoteKind) -> NoteKind:
    return kind


def get_note_life(kind: NoteKind) -> ArchetypeLife:
    result = ArchetypeLife(
        perfect_increment=0,
        great_increment=0,
        good_increment=0,
        miss_increment=0,
    )
    match kind:
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result.miss_increment = -80
        case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK | NoteKind.DAMAGE:
            result.miss_increment = -40
        case NoteKind.ANCHOR:
            pass
        case _:
            assert_never(kind)
    return result


def mirror_flick_direction(direction: FlickDirection) -> FlickDirection:
    match direction:
        case FlickDirection.UP_OMNI:
            return FlickDirection.UP_OMNI
        case FlickDirection.DOWN_OMNI:
            return FlickDirection.DOWN_OMNI
        case FlickDirection.UP_LEFT:
            return FlickDirection.UP_RIGHT
        case FlickDirection.UP_RIGHT:
            return FlickDirection.UP_LEFT
        case FlickDirection.DOWN_LEFT:
            return FlickDirection.DOWN_RIGHT
        case FlickDirection.DOWN_RIGHT:
            return FlickDirection.DOWN_LEFT
        case _:
            assert_never(direction)


def get_visual_spawn_time(
    timescale_group: int | EntityRef,
    target_scaled_time: float,
):
    return min(
        group_scaled_time_to_first_time(timescale_group, target_scaled_time - preempt_time()),
        group_scaled_time_to_first_time_2(timescale_group, target_scaled_time + preempt_time()),
        -2 if 0 <= progress_to(target_scaled_time, -2) <= 2 else 1e8,
    )


def get_attach_params(
    ease_type: EaseType,
    head_lane: float,
    head_size: float,
    head_target_time: float,
    tail_lane: float,
    tail_size: float,
    tail_target_time: float,
    target_time: float,
):
    if abs(head_target_time - tail_target_time) < 1e-6:
        frac = 0.5
    else:
        frac = remap_clamped(head_target_time, tail_target_time, 0.0, 1.0, target_time)
    eased_frac = ease(ease_type, frac)
    lane = lerp(head_lane, tail_lane, eased_frac)
    size = lerp(head_size, tail_size, eased_frac)
    return lane, size


def draw_note(kind: NoteKind, lane: float, size: float, progress: float, direction: FlickDirection, target_time: float):
    if not Layout.progress_start <= progress <= Layout.progress_cutoff:
        return
    travel = approach(progress)
    draw_note_body(kind, lane, size, travel, target_time)
    draw_note_arrow(kind, lane, size, travel, target_time, direction)
    draw_note_tick(kind, lane, travel, target_time)


def draw_slide_note_head(kind: NoteKind, lane: float, size: float, target_time: float):
    if Options.hidden > 0:
        return
    draw_note_body(kind, lane, size, 1.0, target_time)
    draw_note_tick(kind, lane, 1.0, target_time)


def draw_note_body(kind: NoteKind, lane: float, size: float, travel: float, target_time: float):
    match kind:
        case NoteKind.NORM_TAP:
            _draw_regular_body(normal_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            _draw_flick_body(flick_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            _draw_slim_body(normal_trace_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            _draw_slim_body(trace_flick_note_body_sprites, lane, size, travel, target_time)
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            _draw_regular_body(slide_note_body_sprites, lane, size, travel, target_time)
        case (
            NoteKind.CRIT_TAP
            | NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            _draw_regular_body(critical_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            _draw_flick_body(critical_note_body_sprites, lane, size, travel, target_time)
        case (
            NoteKind.CRIT_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
        ):
            _draw_slim_body(critical_trace_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            _draw_slim_body(trace_slide_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.DAMAGE:
            _draw_slim_body(damage_note_body_sprites, lane, size, travel, target_time)
        case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK | NoteKind.ANCHOR:
            pass
        case _:
            assert_never(kind)


def draw_note_arrow(
    kind: NoteKind, lane: float, size: float, travel: float, target_time: float, direction: FlickDirection
):
    match kind:
        case (
            NoteKind.NORM_FLICK
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE_FLICK
        ):
            _draw_arrow(normal_arrow_sprites, lane, size, travel, target_time, direction)
        case (
            NoteKind.CRIT_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
        ):
            _draw_arrow(critical_arrow_sprites, lane, size, travel, target_time, direction)
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            pass
        case _:
            assert_never(kind)


def draw_note_tick(kind: NoteKind, lane: float, travel: float, target_time: float):
    match kind:
        case NoteKind.NORM_TICK:
            _draw_tick(normal_tick_sprites, lane, travel, target_time)
        case NoteKind.CRIT_TICK:
            _draw_tick(critical_tick_sprites, lane, travel, target_time)
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            _draw_tick(normal_trace_tick_sprites, lane, travel, target_time)
        case (
            NoteKind.CRIT_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
        ):
            _draw_tick(critical_trace_tick_sprites, lane, travel, target_time)
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            _draw_tick(trace_flick_tick_sprites, lane, travel, target_time)
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            pass
        case _:
            assert_never(kind)


def _draw_regular_body(sprites: BodySprites, lane: float, size: float, travel: float, target_time: float):
    a = get_alpha(target_time)
    z = get_z(LAYER_NOTE_BODY, time=target_time, lane=lane)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_regular_note_body(lane, size, travel)
        sprites.left.draw(left_layout, z=z, a=a)
        sprites.middle.draw(middle_layout, z=z, a=a)
        sprites.right.draw(right_layout, z=z, a=a)
    else:
        layout = layout_regular_note_body_fallback(lane, size, travel)
        sprites.fallback.draw(layout, z=z, a=a)


def _draw_flick_body(sprites: BodySprites, lane: float, size: float, travel: float, target_time: float):
    a = get_alpha(target_time)
    z = get_z(LAYER_NOTE_FLICK_BODY, time=target_time, lane=lane)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_regular_note_body(lane, size, travel)
        sprites.left.draw(left_layout, z=z, a=a)
        sprites.middle.draw(middle_layout, z=z, a=a)
        sprites.right.draw(right_layout, z=z, a=a)
    else:
        layout = layout_regular_note_body_fallback(lane, size, travel)
        sprites.fallback.draw(layout, z=z, a=a)


def _draw_slim_body(sprites: BodySprites, lane: float, size: float, travel: float, target_time: float):
    a = get_alpha(target_time)
    z = get_z(LAYER_NOTE_SLIM_BODY, time=target_time, lane=lane)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_slim_note_body(lane, size, travel)
        sprites.left.draw(left_layout, z=z, a=a)
        sprites.middle.draw(middle_layout, z=z, a=a)
        sprites.right.draw(right_layout, z=z, a=a)
    else:
        layout = layout_slim_note_body_fallback(lane, size, travel)
        sprites.fallback.draw(layout, z=z, a=a)


def _draw_tick(sprites: TickSprites, lane: float, travel: float, target_time: float):
    a = get_alpha(target_time)
    z = get_z(LAYER_NOTE_TICK, time=target_time, lane=lane)
    layout = layout_tick(lane, travel)
    if sprites.custom_available:
        sprites.normal.draw(layout, z=z, a=a)
    else:
        sprites.fallback.draw(layout, z=z, a=a)


def _draw_arrow(
    sprites: ArrowSprites, lane: float, size: float, travel: float, target_time: float, direction: FlickDirection
):
    match direction:
        case _ if Options.marker_animation:
            period = 0.5
            animation_progress = (time() / period) % 1
        case FlickDirection.UP_LEFT | FlickDirection.UP_OMNI | FlickDirection.UP_RIGHT:
            animation_progress = 0.2
        case FlickDirection.DOWN_LEFT | FlickDirection.DOWN_OMNI | FlickDirection.DOWN_RIGHT:
            animation_progress = 0.8
        case _:
            assert_never(direction)
    animation_alpha = (1 - ease_in_cubic(animation_progress)) if Options.marker_animation else 1
    a = get_alpha(target_time) * animation_alpha
    z = get_z(LAYER_NOTE_ARROW, time=target_time, lane=lane)
    if sprites.custom_available:
        layout = layout_flick_arrow(lane, size, direction, travel, animation_progress)
        sprites.get_sprite(size, direction).draw(layout, z=z, a=a)
    else:
        layout = layout_flick_arrow_fallback(lane, size, direction, travel, animation_progress)
        sprites.fallback.draw(layout, z=z, a=a)


def get_note_particles(kind: NoteKind) -> NoteParticleSet:
    result = +NoteParticleSet
    match kind:
        case NoteKind.NORM_TAP:
            result @= normal_note_particles
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            result @= slide_note_particles
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            result @= flick_note_particles
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            result @= trace_note_particles
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            result @= trace_flick_note_particles
        case NoteKind.CRIT_TAP:
            result @= critical_note_particles
        case (
            NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result @= critical_slide_note_particles
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            result @= critical_flick_note_particles
        case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE | NoteKind.CRIT_TAIL_TRACE:
            result @= critical_trace_note_particles
        case NoteKind.CRIT_TRACE_FLICK | NoteKind.CRIT_HEAD_TRACE_FLICK | NoteKind.CRIT_TAIL_TRACE_FLICK:
            result @= critical_trace_flick_note_particles
        case NoteKind.NORM_TICK:
            result @= normal_tick_particles
        case NoteKind.CRIT_TICK:
            result @= critical_tick_particles
        case NoteKind.HIDE_TICK | NoteKind.ANCHOR:
            result @= empty_note_particles
        case NoteKind.DAMAGE:
            result @= damage_note_particles
        case _:
            assert_never(kind)
    return result


def get_note_effect(kind: NoteKind, judgment: Judgment, accuracy: float):
    result = Effect(-1)
    match kind:
        case (
            NoteKind.NORM_TAP
            | NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            match judgment:
                case Judgment.PERFECT:
                    result @= Effects.normal_perfect
                case Judgment.GREAT:
                    result @= Effects.normal_great
                case Judgment.GOOD:
                    result @= Effects.normal_good
                case Judgment.MISS:
                    result @= Effects.normal_good
                case _:
                    assert_never(judgment)
        case (
            NoteKind.NORM_FLICK
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE_FLICK
        ):
            match judgment:
                case Judgment.PERFECT:
                    result @= Effects.flick_perfect
                case Judgment.GREAT:
                    result @= Effects.flick_great
                case Judgment.GOOD:
                    result @= Effects.flick_good
                case Judgment.MISS:
                    result @= Effects.flick_good
                case _:
                    assert_never(judgment)
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.normal_trace, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteKind.NORM_TICK:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.normal_tick, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteKind.CRIT_TAP:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_tap, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case (
            NoteKind.CRIT_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
        ):
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_flick, Effects.flick_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE | NoteKind.CRIT_TAIL_TRACE:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_trace, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteKind.CRIT_TICK:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_tick, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteKind.HIDE_TICK | NoteKind.ANCHOR:
            result @= EMPTY_EFFECT
        case NoteKind.DAMAGE:
            if judgment == Judgment.MISS:
                result @= Effects.normal_good
            else:
                result @= EMPTY_EFFECT
        case _:
            assert_never(kind)
    return result


def get_note_slot_sprite(kind: NoteKind) -> Sprite:
    result = Sprite(-1)
    match kind:
        case NoteKind.NORM_TAP:
            result @= Skin.normal_slot
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            result @= Skin.flick_slot
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            result @= Skin.slide_slot
        case NoteKind.CRIT_TAP:
            result @= Skin.critical_slot
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            result @= Skin.critical_flick_slot
        case (
            NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result @= Skin.critical_slide_slot
        case (
            NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.DAMAGE
            | NoteKind.ANCHOR
        ):
            result @= Sprite(-1)
        case _:
            assert_never(kind)
    return result


def get_note_slot_glow_sprite(kind: NoteKind) -> Sprite:
    result = Sprite(-1)
    match kind:
        case NoteKind.NORM_TAP:
            result @= Skin.normal_slot_glow
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            result @= Skin.flick_slot_glow
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            result @= Skin.slide_slot_glow
        case NoteKind.CRIT_TAP:
            result @= Skin.critical_slot_glow
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            result @= Skin.critical_flick_slot_glow
        case (
            NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result @= Skin.critical_slide_slot_glow
        case (
            NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.DAMAGE
            | NoteKind.ANCHOR
        ):
            result @= Sprite(-1)
        case _:
            assert_never(kind)
    return result


def play_note_hit_effects(
    kind: NoteKind, lane: float, size: float, direction: FlickDirection, judgment: Judgment, accuracy: float = 0
):
    if kind == NoteKind.DAMAGE and judgment == Judgment.PERFECT:
        return
    sfx = get_note_effect(kind, judgment, accuracy)
    particles = get_note_particles(kind)
    if Options.sfx_enabled and not Options.auto_sfx and not is_watch() and sfx.is_available:
        sfx.play(SFX_DISTANCE)
    if Options.note_effect_enabled:
        linear_particle = first_available_particle(
            particles.linear,
            particles.linear_fallback,
        )
        if linear_particle.is_available:
            layout = layout_linear_effect(lane, shear=0)
            linear_particle.spawn(layout, duration=0.5)
        circular_particle = first_available_particle(
            particles.circular,
            particles.circular_fallback,
        )
        if circular_particle.is_available:
            layout = layout_circular_effect(lane, w=1.75, h=1.05)
            circular_particle.spawn(layout, duration=0.6)
        if particles.directional.is_available:
            match direction:
                case FlickDirection.UP_OMNI | FlickDirection.DOWN_OMNI:
                    shear = 0
                case FlickDirection.UP_LEFT | FlickDirection.DOWN_RIGHT:
                    shear = -1
                case FlickDirection.UP_RIGHT | FlickDirection.DOWN_LEFT:
                    shear = 1
                case _:
                    assert_never(direction)
            layout = layout_rotated_linear_effect(lane, shear=shear)
            particles.directional.spawn(layout, duration=0.32)
        if particles.tick.is_available:
            layout = layout_tick_effect(lane)
            particles.tick.spawn(layout, duration=0.6)
        if particles.slot_linear.is_available:
            for slot_lane in iter_slot_lanes(lane, size):
                layout = layout_linear_effect(slot_lane, shear=0)
                particles.slot_linear.spawn(layout, duration=0.5)
    if Options.lane_effect_enabled:
        layout = layout_lane(lane, size)
        if particles.lane.is_available:
            particles.lane.spawn(layout, duration=1)
        elif particles.lane_basic.is_available:
            particles.lane_basic.spawn(layout, duration=0.3)
    if Options.slot_effect_enabled and not is_watch():
        schedule_note_slot_effects(kind, lane, size, time())


def schedule_note_auto_sfx(kind: NoteKind, target_time: float, accuracy: float = 0):
    if not Options.sfx_enabled:
        return
    if not Options.auto_sfx:
        return
    sfx = get_note_effect(kind, Judgment.PERFECT, accuracy)
    if sfx.is_available:
        sfx.schedule(target_time, SFX_DISTANCE)


def schedule_note_sfx(kind: NoteKind, judgment: Judgment, target_time: float, accuracy: float = 0):
    if not Options.sfx_enabled:
        return
    sfx = get_note_effect(kind, judgment, accuracy)
    if sfx.is_available:
        sfx.schedule(target_time, SFX_DISTANCE)


def schedule_note_slot_effects(kind: NoteKind, lane: float, size: float, target_time: float):
    if is_tutorial():
        return
    if not Options.slot_effect_enabled:
        return
    slot_sprite = get_note_slot_sprite(kind)
    if slot_sprite.is_available:
        for slot_lane in iter_slot_lanes(lane, size):
            get_archetype_by_name(archetype_names.SLOT_EFFECT).spawn(
                sprite=slot_sprite, start_time=target_time, lane=slot_lane
            )
    slot_glow_sprite = get_note_slot_glow_sprite(kind)
    if slot_glow_sprite.is_available:
        get_archetype_by_name(archetype_names.SLOT_GLOW_EFFECT).spawn(
            sprite=slot_glow_sprite, start_time=target_time, lane=lane, size=size
        )


def draw_tutorial_note_slot_effects(kind: NoteKind, lane: float, size: float, start_time: float):
    slot_sprite = get_note_slot_sprite(kind)
    if slot_sprite.is_available and time() < start_time + SLOT_EFFECT_DURATION:
        for slot_lane in iter_slot_lanes(lane, size):
            draw_slot_effect(
                sprite=slot_sprite,
                start_time=start_time,
                end_time=start_time + SLOT_EFFECT_DURATION,
                lane=slot_lane,
            )
    slot_glow_sprite = get_note_slot_glow_sprite(kind)
    if slot_glow_sprite.is_available and time() < start_time + SLOT_GLOW_EFFECT_DURATION:
        draw_slot_glow_effect(
            sprite=slot_glow_sprite,
            start_time=start_time,
            end_time=start_time + SLOT_GLOW_EFFECT_DURATION,
            lane=lane,
            size=size,
        )


def get_note_window(kind: NoteKind) -> JudgmentWindow:
    result = +JudgmentWindow
    match kind:
        case NoteKind.NORM_TAP | NoteKind.NORM_HEAD_TAP | NoteKind.NORM_TAIL_TAP:
            result @= TAP_NORMAL_WINDOW
        case NoteKind.CRIT_TAP | NoteKind.CRIT_HEAD_TAP | NoteKind.CRIT_TAIL_TAP:
            result @= TAP_CRITICAL_WINDOW
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK:
            result @= FLICK_NORMAL_WINDOW
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK:
            result @= FLICK_CRITICAL_WINDOW
        case NoteKind.NORM_TAIL_FLICK:
            result @= SLIDE_END_FLICK_NORMAL_WINDOW
        case NoteKind.CRIT_TAIL_FLICK:
            result @= SLIDE_END_FLICK_CRITICAL_WINDOW
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE:
            result @= TRACE_NORMAL_WINDOW
        case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE:
            result @= TRACE_CRITICAL_WINDOW
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            result @= TRACE_FLICK_NORMAL_WINDOW
        case NoteKind.CRIT_TRACE_FLICK | NoteKind.CRIT_HEAD_TRACE_FLICK | NoteKind.CRIT_TAIL_TRACE_FLICK:
            result @= TRACE_FLICK_CRITICAL_WINDOW
        case NoteKind.NORM_RELEASE | NoteKind.NORM_HEAD_RELEASE | NoteKind.NORM_TAIL_RELEASE:
            result @= SLIDE_END_NORMAL_WINDOW
        case NoteKind.CRIT_RELEASE | NoteKind.CRIT_HEAD_RELEASE | NoteKind.CRIT_TAIL_RELEASE:
            result @= SLIDE_END_CRITICAL_WINDOW
        case NoteKind.NORM_TAIL_TRACE:
            result @= SLIDE_END_TRACE_NORMAL_WINDOW
        case NoteKind.CRIT_TAIL_TRACE:
            result @= SLIDE_END_TRACE_CRITICAL_WINDOW
        case NoteKind.NORM_TAIL_TRACE_FLICK:
            result @= TRACE_FLICK_NORMAL_WINDOW
        case NoteKind.CRIT_TAIL_TRACE_FLICK:
            result @= TRACE_FLICK_CRITICAL_WINDOW
        case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK | NoteKind.ANCHOR | NoteKind.DAMAGE:
            result @= EMPTY_JUDGMENT_WINDOW
        case _:
            assert_never(kind)
    return result


def get_note_window_bad(kind: NoteKind) -> Interval:
    result = +Interval
    match kind:
        case NoteKind.NORM_TAP | NoteKind.NORM_HEAD_TAP | NoteKind.NORM_TAIL_TAP:
            result @= TAP_NORMAL_WINDOW_BAD
        case NoteKind.CRIT_TAP | NoteKind.CRIT_HEAD_TAP | NoteKind.CRIT_TAIL_TAP:
            result @= TAP_CRITICAL_WINDOW_BAD
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK:
            result @= FLICK_NORMAL_WINDOW_BAD
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK:
            result @= FLICK_NORMAL_WINDOW_BAD
        case NoteKind.DAMAGE:
            result @= Interval(-999, 999)
        case (
            NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TRACE
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
        ):
            result @= Interval(0, 0)
        case _:
            assert_never(kind)
    return result


def get_note_bucket(kind: NoteKind) -> Bucket:
    result = Bucket(-1)
    match kind:
        case NoteKind.NORM_TAP:
            result @= Buckets.normal_tap
        case NoteKind.CRIT_TAP:
            result @= Buckets.critical_tap
        case NoteKind.NORM_FLICK:
            result @= Buckets.normal_flick
        case NoteKind.CRIT_FLICK:
            result @= Buckets.critical_flick
        case NoteKind.NORM_TRACE:
            result @= Buckets.normal_trace
        case NoteKind.CRIT_TRACE:
            result @= Buckets.critical_trace
        case NoteKind.NORM_TRACE_FLICK:
            result @= Buckets.normal_trace_flick
        case NoteKind.CRIT_TRACE_FLICK:
            result @= Buckets.critical_trace_flick
        case NoteKind.NORM_HEAD_TAP:
            result @= Buckets.normal_head_tap
        case NoteKind.CRIT_HEAD_TAP:
            result @= Buckets.critical_head_tap
        case NoteKind.NORM_HEAD_FLICK:
            result @= Buckets.normal_head_flick
        case NoteKind.CRIT_HEAD_FLICK:
            result @= Buckets.critical_head_flick
        case NoteKind.NORM_HEAD_TRACE:
            result @= Buckets.normal_head_trace
        case NoteKind.CRIT_HEAD_TRACE:
            result @= Buckets.critical_head_trace
        case NoteKind.NORM_HEAD_TRACE_FLICK:
            result @= Buckets.normal_head_trace_flick
        case NoteKind.CRIT_HEAD_TRACE_FLICK:
            result @= Buckets.critical_head_trace_flick
        case NoteKind.NORM_TAIL_FLICK:
            result @= Buckets.normal_tail_flick
        case NoteKind.CRIT_TAIL_FLICK:
            result @= Buckets.critical_tail_flick
        case NoteKind.NORM_TAIL_TRACE:
            result @= Buckets.normal_tail_trace
        case NoteKind.CRIT_TAIL_TRACE:
            result @= Buckets.critical_tail_trace
        case NoteKind.NORM_TAIL_TRACE_FLICK:
            result @= Buckets.normal_tail_trace_flick
        case NoteKind.CRIT_TAIL_TRACE_FLICK:
            result @= Buckets.critical_tail_trace_flick
        case NoteKind.NORM_TAIL_RELEASE:
            result @= Buckets.normal_tail_release
        case NoteKind.CRIT_TAIL_RELEASE:
            result @= Buckets.critical_tail_release
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            result @= Bucket(-1)
        case _:
            assert_never(kind)
    return result


def get_leniency(kind: NoteKind) -> float:
    match kind:
        case NoteKind.NORM_TAP | NoteKind.CRIT_TAP:
            return 0.75
        case (
            NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
        ):
            return 1.0
        case NoteKind.ANCHOR | NoteKind.DAMAGE:
            return 0
        case _:
            assert_never(kind)


def has_tap_input(kind: NoteKind) -> bool:
    match kind:
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
        ):
            return True
        case (
            NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            return False
        case _:
            assert_never(kind)


def has_release_input(kind: NoteKind) -> bool:
    match kind:
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            return True
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            return False
        case _:
            assert_never(kind)


def is_head(kind: NoteKind) -> bool:
    match kind:
        case (
            NoteKind.NORM_HEAD_TAP
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_HEAD_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.NORM_HEAD_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.CRIT_HEAD_RELEASE
        ):
            return True
        case (
            NoteKind.NORM_TAP
            | NoteKind.CRIT_TAP
            | NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_TRACE
            | NoteKind.CRIT_TRACE
            | NoteKind.NORM_TRACE_FLICK
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.NORM_RELEASE
            | NoteKind.CRIT_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
            | NoteKind.NORM_TAIL_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.NORM_TAIL_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
            | NoteKind.NORM_TAIL_RELEASE
            | NoteKind.CRIT_TAIL_RELEASE
            | NoteKind.NORM_TICK
            | NoteKind.CRIT_TICK
            | NoteKind.HIDE_TICK
            | NoteKind.ANCHOR
            | NoteKind.DAMAGE
        ):
            return False
        case _:
            assert_never(kind)
