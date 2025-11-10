from collections.abc import Iterable
from enum import IntEnum, auto
from typing import assert_never, cast

from sonolus.script.archetype import EntityRef, HapticType, PlayArchetype, WatchArchetype, get_archetype_by_name
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
    SLIDE_TICK_JUDGMENT_WINDOW,
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
from sekai.lib.connector import ActiveConnectorKind, ConnectorKind
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
    layout_rotated2_linear_effect,
    layout_slim_note_body,
    layout_slim_note_body_fallback,
    layout_tick,
    layout_tick_effect,
    preempt_time,
    progress_to,
)
from sekai.lib.level_config import LevelConfig
from sekai.lib.options import Options, ScoreMode
from sekai.lib.particle import (
    EMPTY_NOTE_PARTICLE_SET,
    ActiveParticles,
    NoteParticleSet,
    Particles,
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
    damage_tick_sprites,
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
from sekai.lib.timescale import CompositeTime, group_scaled_time_to_first_time, group_scaled_time_to_first_time_2


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


def init_score(note_archetypes: Iterable[type[PlayArchetype | WatchArchetype]]):
    match LevelConfig.score_mode:
        case ScoreMode.WEIGHTED_COMBO | ScoreMode.UNWEIGHTED_COMBO:
            level_score().update(
                perfect_multiplier=1.0,
                great_multiplier=0.7,
                good_multiplier=0.5,
                consecutive_great_multiplier=0.1,  # Note that the base tap note multiplier is 10 not 1
                consecutive_great_step=100,
                consecutive_great_cap=1000,
            )
        case ScoreMode.WEIGHTED_FLAT | ScoreMode.UNWEIGHTED_FLAT:
            level_score().update(
                perfect_multiplier=3.0,
                great_multiplier=2.0,
                good_multiplier=1.0,
            )
        case _:
            assert_never(LevelConfig.score_mode)

    match LevelConfig.score_mode:
        case ScoreMode.WEIGHTED_COMBO | ScoreMode.WEIGHTED_FLAT:
            for note_archetype in note_archetypes:
                kind = cast(NoteKind, note_archetype.key)
                match kind:
                    case NoteKind.NORM_TAP | NoteKind.NORM_HEAD_TAP | NoteKind.NORM_TAIL_TAP:
                        weight = 10
                    case NoteKind.CRIT_TAP | NoteKind.CRIT_HEAD_TAP | NoteKind.CRIT_TAIL_TAP:
                        weight = 20
                    case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
                        weight = 10
                    case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
                        weight = 30
                    case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
                        weight = 1
                    case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE | NoteKind.CRIT_TAIL_TRACE:
                        weight = 2
                    case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
                        weight = 10
                    case NoteKind.CRIT_TRACE_FLICK | NoteKind.CRIT_HEAD_TRACE_FLICK | NoteKind.CRIT_TAIL_TRACE_FLICK:
                        weight = 30
                    case NoteKind.NORM_RELEASE | NoteKind.NORM_HEAD_RELEASE | NoteKind.NORM_TAIL_RELEASE:
                        weight = 10
                    case NoteKind.CRIT_RELEASE | NoteKind.CRIT_HEAD_RELEASE | NoteKind.CRIT_TAIL_RELEASE:
                        weight = 20
                    case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK:
                        weight = 1
                    case NoteKind.DAMAGE:
                        weight = 1
                    case NoteKind.ANCHOR:
                        weight = 1  # Doesn't really matter since anchors are not scored
                    case _:
                        assert_never(kind)
                note_archetype.archetype_score_multiplier = weight
        case ScoreMode.UNWEIGHTED_COMBO | ScoreMode.UNWEIGHTED_FLAT:
            for note_archetype in note_archetypes:
                note_archetype.archetype_score_multiplier = 10
        case _:
            assert_never(LevelConfig.score_mode)


def init_life(
    note_archetypes: Iterable[type[PlayArchetype | WatchArchetype]],
    initial_life: int,
):
    for note_archetype in note_archetypes:
        init_note_life(note_archetype)
    level_life().update(initial=initial_life, maximum=initial_life)


def init_note_life(archetype: type[PlayArchetype | WatchArchetype]):
    kind = cast(NoteKind, archetype.key)
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
            archetype.life.miss_increment = -80
        case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK | NoteKind.DAMAGE:
            archetype.life.miss_increment = -40
        case NoteKind.ANCHOR:
            pass
        case _:
            assert_never(kind)


def map_note_kind(kind: NoteKind) -> NoteKind:
    return kind


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
    target_scaled_time: CompositeTime | float,
):
    if isinstance(target_scaled_time, CompositeTime):
        target_scaled_time = target_scaled_time.total
    return min(
        group_scaled_time_to_first_time(timescale_group, target_scaled_time - preempt_time() * 1.1),
        group_scaled_time_to_first_time_2(timescale_group, target_scaled_time + preempt_time() * 1.1),
        -2 if -1 <= progress_to(target_scaled_time, -2) <= 3 else 1e8,
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
    sprite_set = get_note_sprite_set(kind, direction)
    draw_note_body(sprite_set.body, kind, lane, size, travel, target_time)
    draw_note_arrow(sprite_set.arrow, lane, size, travel, target_time, direction)
    draw_note_tick(sprite_set.tick, lane, travel, target_time)


def draw_slide_note_head(
    kind: NoteKind, connector_kind: ActiveConnectorKind, lane: float, size: float, target_time: float
):
    if Options.hidden > 0:
        return
    match connector_kind:
        case ConnectorKind.ACTIVE_NORMAL | ConnectorKind.ACTIVE_FAKE_NORMAL:
            kind = note_kind_as_normal(kind)
        case ConnectorKind.ACTIVE_CRITICAL | ConnectorKind.ACTIVE_FAKE_CRITICAL:
            kind = note_kind_as_critical(kind)
        case _:
            assert_never(connector_kind)
    sprite_set = get_note_sprite_set(kind, FlickDirection.UP_OMNI)
    draw_note_body(sprite_set.body, kind, lane, size, 1.0, target_time)
    draw_note_tick(sprite_set.tick, lane, 1.0, target_time)


def note_kind_as_normal(kind: NoteKind) -> NoteKind:
    match kind:
        case NoteKind.CRIT_TAP:
            return NoteKind.NORM_TAP
        case NoteKind.CRIT_FLICK:
            return NoteKind.NORM_FLICK
        case NoteKind.CRIT_TRACE:
            return NoteKind.NORM_TRACE
        case NoteKind.CRIT_TRACE_FLICK:
            return NoteKind.NORM_TRACE_FLICK
        case NoteKind.CRIT_RELEASE:
            return NoteKind.NORM_RELEASE
        case NoteKind.CRIT_HEAD_TAP:
            return NoteKind.NORM_HEAD_TAP
        case NoteKind.CRIT_HEAD_FLICK:
            return NoteKind.NORM_HEAD_FLICK
        case NoteKind.CRIT_HEAD_TRACE:
            return NoteKind.NORM_HEAD_TRACE
        case NoteKind.CRIT_HEAD_TRACE_FLICK:
            return NoteKind.NORM_HEAD_TRACE_FLICK
        case NoteKind.CRIT_HEAD_RELEASE:
            return NoteKind.NORM_HEAD_RELEASE
        case NoteKind.CRIT_TAIL_TAP:
            return NoteKind.NORM_TAIL_TAP
        case NoteKind.CRIT_TAIL_FLICK:
            return NoteKind.NORM_TAIL_FLICK
        case NoteKind.CRIT_TAIL_TRACE:
            return NoteKind.NORM_TAIL_TRACE
        case NoteKind.CRIT_TAIL_TRACE_FLICK:
            return NoteKind.NORM_TAIL_TRACE_FLICK
        case NoteKind.CRIT_TAIL_RELEASE:
            return NoteKind.NORM_TAIL_RELEASE
        case NoteKind.CRIT_TICK:
            return NoteKind.NORM_TICK
        case _:
            return kind


def note_kind_as_critical(kind: NoteKind) -> NoteKind:
    match kind:
        case NoteKind.NORM_TAP:
            return NoteKind.CRIT_TAP
        case NoteKind.NORM_FLICK:
            return NoteKind.CRIT_FLICK
        case NoteKind.NORM_TRACE:
            return NoteKind.CRIT_TRACE
        case NoteKind.NORM_TRACE_FLICK:
            return NoteKind.CRIT_TRACE_FLICK
        case NoteKind.NORM_RELEASE:
            return NoteKind.CRIT_RELEASE
        case NoteKind.NORM_HEAD_TAP:
            return NoteKind.CRIT_HEAD_TAP
        case NoteKind.NORM_HEAD_FLICK:
            return NoteKind.CRIT_HEAD_FLICK
        case NoteKind.NORM_HEAD_TRACE:
            return NoteKind.CRIT_HEAD_TRACE
        case NoteKind.NORM_HEAD_TRACE_FLICK:
            return NoteKind.CRIT_HEAD_TRACE_FLICK
        case NoteKind.NORM_HEAD_RELEASE:
            return NoteKind.CRIT_HEAD_RELEASE
        case NoteKind.NORM_TAIL_TAP:
            return NoteKind.CRIT_TAIL_TAP
        case NoteKind.NORM_TAIL_FLICK:
            return NoteKind.CRIT_TAIL_FLICK
        case NoteKind.NORM_TAIL_TRACE:
            return NoteKind.CRIT_TAIL_TRACE
        case NoteKind.NORM_TAIL_TRACE_FLICK:
            return NoteKind.CRIT_TAIL_TRACE_FLICK
        case NoteKind.NORM_TAIL_RELEASE:
            return NoteKind.CRIT_TAIL_RELEASE
        case NoteKind.NORM_TICK:
            return NoteKind.CRIT_TICK
        case _:
            return kind


def get_note_sprite_set(kind: NoteKind, direction: FlickDirection) -> NoteSpriteSet:
    result = +NoteSpriteSet
    match kind:
        case NoteKind.NORM_TAP:
            result @= ActiveSkin.normal_note
        case NoteKind.CRIT_TAP:
            result @= ActiveSkin.critical_note
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveSkin.flick_note
            else:
                result @= ActiveSkin.down_flick_note
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveSkin.critical_flick_note
            else:
                result @= ActiveSkin.critical_down_flick_note
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            result @= ActiveSkin.trace_note
        case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE | NoteKind.CRIT_TAIL_TRACE:
            result @= ActiveSkin.critical_trace_note
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveSkin.trace_flick_note
            else:
                result @= ActiveSkin.trace_down_flick_note
        case NoteKind.CRIT_TRACE_FLICK | NoteKind.CRIT_HEAD_TRACE_FLICK | NoteKind.CRIT_TAIL_TRACE_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveSkin.critical_trace_flick_note
            else:
                result @= ActiveSkin.critical_trace_down_flick_note
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            result @= ActiveSkin.slide_note
        case (
            NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result @= ActiveSkin.critical_slide_note
        case NoteKind.NORM_TICK:
            result @= ActiveSkin.normal_slide_tick_note
        case NoteKind.CRIT_TICK:
            result @= ActiveSkin.critical_slide_tick_note
        case NoteKind.HIDE_TICK | NoteKind.ANCHOR:
            result @= EMPTY_NOTE_SPRITE_SET
        case NoteKind.DAMAGE:
            result @= ActiveSkin.damage_note
        case _:
            assert_never(kind)
    return result


def get_note_body_layer(kind: NoteKind) -> int:
    match kind:
        case (
            NoteKind.NORM_FLICK
            | NoteKind.CRIT_FLICK
            | NoteKind.NORM_HEAD_FLICK
            | NoteKind.CRIT_HEAD_FLICK
            | NoteKind.NORM_TAIL_FLICK
            | NoteKind.CRIT_TAIL_FLICK
        ):
            return LAYER_NOTE_FLICK_BODY
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
        ):
            _draw_tick(critical_trace_tick_sprites, lane, travel, target_time)
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            _draw_tick(trace_flick_tick_sprites, lane, travel, target_time)
        case NoteKind.DAMAGE:
            if Options.using_damage_tick:
                _draw_tick(damage_tick_sprites, lane, travel, target_time)
            else:
                pass
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
        ):
            pass
        case _:
            return LAYER_NOTE_BODY


def draw_note_body(sprites: BodySpriteSet, kind: NoteKind, lane: float, size: float, travel: float, target_time: float):
    layer = get_note_body_layer(kind)
    a = get_alpha(target_time)
    z = get_z(layer, time=target_time, lane=lane)
    match sprites.render_type:
        case BodyRenderType.NORMAL:
            left_layout, middle_layout, right_layout = layout_regular_note_body(lane, size, travel)
            sprites.left.draw(left_layout, z=z, a=a)
            sprites.middle.draw(middle_layout, z=z, a=a)
            sprites.right.draw(right_layout, z=z, a=a)
        case BodyRenderType.SLIM:
            left_layout, middle_layout, right_layout = layout_slim_note_body(lane, size, travel)
            sprites.left.draw(left_layout, z=z, a=a)
            sprites.middle.draw(middle_layout, z=z, a=a)
            sprites.right.draw(right_layout, z=z, a=a)
        case BodyRenderType.NORMAL_FALLBACK:
            layout = layout_regular_note_body_fallback(lane, size, travel)
            sprites.middle.draw(layout, z=z, a=a)
        case BodyRenderType.SLIM_FALLBACK:
            layout = layout_slim_note_body_fallback(lane, size, travel)
            sprites.middle.draw(layout, z=z, a=a)


def draw_note_tick(sprite: Sprite, lane: float, travel: float, target_time: float):
    a = get_alpha(target_time)
    z = get_z(LAYER_NOTE_TICK, time=target_time, lane=lane)
    layout = layout_tick(lane, travel)
    sprite.draw(layout, z=z, a=a)


def draw_note_arrow(
    sprites: ArrowSpriteSet, lane: float, size: float, travel: float, target_time: float, direction: FlickDirection
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
    match sprites.render_type:
        case ArrowRenderType.NORMAL:
            layout = layout_flick_arrow(lane, size, direction, travel, animation_progress)
            sprites.get_sprite(size, direction).draw(layout, z=z, a=a)
        case ArrowRenderType.FALLBACK:
            layout = layout_flick_arrow_fallback(lane, size, direction, travel, animation_progress)
            sprites.get_sprite(size, direction).draw(layout, z=z, a=a)


def get_note_particles(kind: NoteKind, direction: FlickDirection) -> NoteParticleSet:
    result = +NoteParticleSet
    match kind:
        case NoteKind.NORM_TAP:
            result @= ActiveParticles.normal_note
        case (
            NoteKind.NORM_RELEASE
            | NoteKind.NORM_HEAD_TAP
            | NoteKind.NORM_HEAD_RELEASE
            | NoteKind.NORM_TAIL_TAP
            | NoteKind.NORM_TAIL_RELEASE
        ):
            result @= ActiveParticles.slide_note
        case NoteKind.NORM_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.NORM_TAIL_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveParticles.flick_note
            else:
                result @= ActiveParticles.down_flick_note
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            result @= ActiveParticles.trace_note
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveParticles.trace_flick_note
            else:
                result @= ActiveParticles.trace_down_flick_note
        case NoteKind.CRIT_TAP:
            result @= ActiveParticles.critical_note
        case (
            NoteKind.CRIT_RELEASE
            | NoteKind.CRIT_HEAD_TAP
            | NoteKind.CRIT_HEAD_RELEASE
            | NoteKind.CRIT_TAIL_TAP
            | NoteKind.CRIT_TAIL_RELEASE
        ):
            result @= ActiveParticles.critical_slide_note
        case NoteKind.CRIT_FLICK | NoteKind.CRIT_HEAD_FLICK | NoteKind.CRIT_TAIL_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveParticles.critical_flick_note
            else:
                result @= ActiveParticles.critical_down_flick_note
        case NoteKind.CRIT_TRACE | NoteKind.CRIT_HEAD_TRACE | NoteKind.CRIT_TAIL_TRACE:
            result @= ActiveParticles.critical_trace_note
        case NoteKind.CRIT_TRACE_FLICK | NoteKind.CRIT_HEAD_TRACE_FLICK | NoteKind.CRIT_TAIL_TRACE_FLICK:
            if direction in {FlickDirection.UP_OMNI, FlickDirection.UP_LEFT, FlickDirection.UP_RIGHT}:
                result @= ActiveParticles.critical_trace_flick_note
            else:
                result @= ActiveParticles.critical_trace_down_flick_note
        case NoteKind.NORM_TICK:
            result @= ActiveParticles.normal_slide_tick_note
        case NoteKind.CRIT_TICK:
            result @= ActiveParticles.critical_slide_tick_note
        case NoteKind.HIDE_TICK | NoteKind.ANCHOR:
            result @= EMPTY_NOTE_PARTICLE_SET
        case NoteKind.DAMAGE:
            result @= ActiveParticles.damage_note
        case _:
            assert_never(kind)
    return result


def get_note_effect(kind: NoteKind, judgment: Judgment, accuracy: float):
    result = Effect(-1)
    assert kind != NoteEffectKind.DEFAULT, "Unexpected NoteEffectKind.DEFAULT argument to get_note_effect"
    match kind:
        case NoteEffectKind.NORM_BASIC:
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
        case NoteEffectKind.NORM_FLICK:
            match judgment:
                case Judgment.PERFECT:
                    result @= Effects.flick_perfect
                case Judgment.GREAT:
                    result @= Effects.flick_perfect
                case Judgment.GOOD:
                    result @= Effects.flick_perfect
                case Judgment.MISS:
                    result @= Effects.flick_perfect
                case _:
                    assert_never(judgment)
        case NoteEffectKind.NORM_TRACE:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.normal_trace, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.NORM_TICK:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.normal_tick, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.CRIT_BASIC:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_tap, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.CRIT_FLICK:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_flick, Effects.flick_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.CRIT_TRACE:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_trace, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.CRIT_TICK:
            if judgment != Judgment.MISS:
                result @= first_available_effect(Effects.critical_tick, Effects.normal_perfect)
            else:
                result @= EMPTY_EFFECT
        case NoteEffectKind.NONE:
            result @= EMPTY_EFFECT
        case NoteEffectKind.DAMAGE:
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


def get_note_slot_glow_sprite(kind: NoteKind, judgment: Judgment = Judgment.PERFECT) -> Sprite:
    result = Sprite(-1)
    match kind:
        case NoteKind.NORM_TAP:
            match judgment:
                case Judgment.PERFECT:
                    result @= Skin.normal_slot_glow
                case Judgment.GREAT:
                    result @= Skin.normal_slot_glow_great
                case Judgment.GOOD | Judgment.MISS:
                    result @= Skin.normal_slot_glow_good
                case _:
                    assert_never(kind)
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
    kind: NoteKind,
    effect_kind: NoteEffectKind,
    lane: float,
    size: float,
    direction: FlickDirection,
    judgment: Judgment,
):
    if kind == NoteKind.DAMAGE and judgment == Judgment.PERFECT:
        return
    sfx = get_note_effect(effect_kind, judgment)
    particles = get_note_particles(kind)
    if Options.sfx_enabled and not Options.auto_sfx and not is_watch() and sfx.is_available:
        sfx.play(SFX_DISTANCE)
    if Options.note_effect_enabled:
        linear = +particles.linear
        circular = +particles.circular
        slot_linear = +particles.slot_linear
        if kind == NoteKind.NORM_TAP:
            match judgment:
                case Judgment.GREAT:
                    linear @= particles.linear_great
                    circular @= particles.circular_great
                    slot_linear @= particles.slot_linear_great
                case Judgment.GOOD | Judgment.MISS:
                    linear @= particles.linear_good
                    circular @= particles.circular_good
                    slot_linear @= particles.slot_linear_good
        linear_particle = first_available_particle(
            linear,
            particles.linear,
            particles.linear_fallback,
        )
        if linear_particle.is_available:
            layout = +layout_linear_effect(lane, shear=0)
            if linear_particle.id == Particles.normal_note_linear_good.id:
                for slot_lane in iter_slot_lanes(lane, size):
                    layout @= layout_linear_effect(slot_lane, shear=0)
                    linear_particle.spawn(layout, duration=0.5 * Options.note_effect_duration)
            else:
                linear_particle.spawn(layout, duration=0.5 * Options.note_effect_duration)
        circular_particle = first_available_particle(
            circular,
            particles.circular,
            particles.circular_fallback,
        )
        if circular_particle.is_available:
            layout = +layout_circular_effect(lane, w=1.75, h=1.05)
            if linear_particle.id == Particles.normal_note_circular_good.id:
                for slot_lane in iter_slot_lanes(lane, size):
                    layout @= layout_circular_effect(slot_lane, w=1.75, h=1.05)
                circular_particle.spawn(layout, duration=0.6 * Options.note_effect_duration)
            else:
                circular_particle.spawn(layout, duration=0.6 * Options.note_effect_duration)
        if particles.directional.is_available:
            degree = (
                45
                if kind
                in (
                    NoteKind.CRIT_FLICK,
                    NoteKind.CRIT_HEAD_FLICK,
                    NoteKind.CRIT_HEAD_TRACE_FLICK,
                    NoteKind.CRIT_TAIL_FLICK,
                    NoteKind.CRIT_TAIL_TRACE_FLICK,
                )
                and Options.version == 1
                else 22.5
            )
            match direction:
                case FlickDirection.UP_OMNI | FlickDirection.DOWN_OMNI:
                    shear = 0
                case FlickDirection.UP_LEFT | FlickDirection.DOWN_RIGHT:
                    shear = degree
                case FlickDirection.UP_RIGHT | FlickDirection.DOWN_LEFT:
                    shear = -degree
                case _:
                    assert_never(direction)
            layout = layout_rotated2_linear_effect(lane, degree=shear)
            particles.directional.spawn(layout, duration=0.32 * Options.note_effect_duration)
        if particles.tick.is_available:
            layout = layout_tick_effect(lane)
            particles.tick.spawn(layout, duration=0.6 * Options.note_effect_duration)
        slot_linear_particle = first_available_particle(
            slot_linear,
            particles.slot_linear,
        )
        if slot_linear_particle.is_available:
            for slot_lane in iter_slot_lanes(lane, size):
                layout = layout_linear_effect(slot_lane, shear=0)
                slot_linear_particle.spawn(layout, duration=0.5 * Options.note_effect_duration)
    if Options.lane_effect_enabled:
        if particles.lane.is_available:
            if particles.lane.id != Particles.critical_flick_note_lane_linear.id:
                for slot_lane in iter_slot_lanes(lane, size):
                    layout = layout_lane(slot_lane, 0.5)
                    particles.lane.spawn(layout, duration=1 * Options.note_effect_duration)
        elif particles.lane_basic.is_available:
            for slot_lane in iter_slot_lanes(lane, size):
                layout = layout_lane(slot_lane, 0.5)
                particles.lane_basic.spawn(layout, duration=0.3 * Options.note_effect_duration)
    if Options.slot_effect_enabled and not is_watch():
        schedule_note_slot_effects(kind, lane, size, time(), judgment)


def schedule_note_auto_sfx(kind: NoteKind, target_time: float, accuracy: float = 0):
    if not Options.sfx_enabled:
        return
    if not Options.auto_sfx:
        return
    sfx = get_note_effect(kind, Judgment.PERFECT)
    if sfx.is_available:
        sfx.schedule(target_time, SFX_DISTANCE)


def schedule_note_sfx(kind: NoteEffectKind, judgment: Judgment, target_time: float):
    if not Options.sfx_enabled:
        return
    sfx = get_note_effect(kind, judgment)
    if sfx.is_available:
        sfx.schedule(target_time, SFX_DISTANCE)


def schedule_note_slot_effects(
    kind: NoteKind, lane: float, size: float, target_time: float, judgment: Judgment = Judgment.PERFECT
):
    if is_tutorial():
        return
    if not Options.slot_effect_enabled:
        return
    sprite_set = get_note_sprite_set(kind, direction)
    slot_sprite = sprite_set.slot
    if slot_sprite.is_available:
        for slot_lane in iter_slot_lanes(lane, size):
            get_archetype_by_name(archetype_names.SLOT_EFFECT).spawn(
                sprite=slot_sprite, start_time=target_time, lane=slot_lane
            )
    slot_glow_sprite = get_note_slot_glow_sprite(kind, judgment)
    if slot_glow_sprite.is_available:
        for slot_lane in iter_slot_lanes(lane, size):
            get_archetype_by_name(archetype_names.SLOT_GLOW_EFFECT).spawn(
                sprite=slot_glow_sprite, start_time=target_time, lane=slot_lane, size=size
            )


def draw_tutorial_note_slot_effects(kind: NoteKind, lane: float, size: float, start_time: float):
    slot_sprite = get_note_slot_sprite(kind)
    if slot_sprite.is_available and time() < start_time + SLOT_EFFECT_DURATION * Options.note_effect_duration:
        for slot_lane in iter_slot_lanes(lane, size):
            draw_slot_effect(
                sprite=slot_sprite,
                start_time=start_time,
                end_time=start_time + SLOT_EFFECT_DURATION * Options.note_effect_duration,
                lane=slot_lane,
            )
    slot_glow_sprite = get_note_slot_glow_sprite(kind)
    if slot_glow_sprite.is_available and time() < start_time + SLOT_GLOW_EFFECT_DURATION * Options.note_effect_duration:
        draw_slot_glow_effect(
            sprite=slot_glow_sprite,
            start_time=start_time,
            end_time=start_time + SLOT_GLOW_EFFECT_DURATION * Options.note_effect_duration,
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
        case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK:
            result @= SLIDE_TICK_JUDGMENT_WINDOW
        case NoteKind.ANCHOR | NoteKind.DAMAGE:
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
            result @= Interval(0, 0)
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
            result @= Interval(-1, -1)
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
