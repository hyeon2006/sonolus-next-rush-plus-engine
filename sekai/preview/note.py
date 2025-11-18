from __future__ import annotations

from typing import cast

from sonolus.script.archetype import EntityRef, PreviewArchetype, StandardImport, entity_data, imported
from sonolus.script.interval import unlerp_clamped
from sonolus.script.sprite import Sprite
from sonolus.script.timing import beat_to_time

from sekai.lib.connector import ConnectorKind, ConnectorLayer
from sekai.lib.ease import EaseType
from sekai.lib.layer import (
    LAYER_NOTE_ARROW,
    LAYER_NOTE_TICK,
    get_z,
)
from sekai.lib.layout import FlickDirection
from sekai.lib.note import (
    NoteKind,
    get_attach_params,
    get_note_body_layer,
    get_note_sprite_set,
    map_note_kind,
    mirror_flick_direction,
)
from sekai.lib.options import Options
from sekai.lib.skin import ArrowRenderType, ArrowSpriteSet, BodyRenderType, BodySpriteSet
from sekai.play.note import derive_note_archetypes
from sekai.preview.layout import (
    PREVIEW_COLUMN_SECS,
    PreviewData,
    get_adjusted_time,
    layout_preview_flick_arrow,
    layout_preview_flick_arrow_fallback,
    layout_preview_regular_note_body,
    layout_preview_regular_note_body_fallback,
    layout_preview_slim_note_body,
    layout_preview_slim_note_body_fallback,
    layout_preview_tick,
    time_to_preview_col,
    time_to_preview_y,
)


class PreviewBaseNote(PreviewArchetype):
    beat: StandardImport.BEAT
    lane: float = imported()
    size: float = imported()
    direction: FlickDirection = imported()
    active_head_ref: EntityRef[PreviewBaseNote] = imported(name="activeHead")
    is_attached: bool = imported(name="isAttached")
    connector_ease: EaseType = imported(name="connectorEase")
    segment_kind: ConnectorKind = imported(name="segmentKind")
    segment_alpha: float = imported(name="segmentAlpha")
    segment_layer: ConnectorLayer = imported(name="segmentLayer")
    attach_head_ref: EntityRef[PreviewBaseNote] = imported(name="attachHead")
    attach_tail_ref: EntityRef[PreviewBaseNote] = imported(name="attachTail")

    kind: NoteKind = entity_data()
    data_init_done: bool = entity_data()
    target_time: float = entity_data()

    def init_data(self):
        if self.data_init_done:
            return

        self.kind = map_note_kind(cast(NoteKind, self.key))

        self.data_init_done = True

        if Options.mirror:
            self.lane *= -1
            self.direction = mirror_flick_direction(self.direction)

        self.target_time = beat_to_time(self.beat)

    def preprocess(self):
        self.init_data()

        if self.is_attached:
            attach_head = self.attach_head_ref.get()
            attach_tail = self.attach_tail_ref.get()
            attach_head.init_data()
            attach_tail.init_data()
            self.connector_ease = attach_head.connector_ease
            lane, size = get_attach_params(
                ease_type=attach_head.connector_ease,
                head_lane=attach_head.lane,
                head_size=attach_head.size,
                head_target_time=attach_head.target_time,
                tail_lane=attach_tail.lane,
                tail_size=attach_tail.size,
                tail_target_time=attach_tail.target_time,
                target_time=self.target_time,
            )
            self.lane = lane
            self.size = size

        PreviewData.max_time = max(PreviewData.max_time, self.target_time)
        PreviewData.max_beat = max(PreviewData.max_beat, self.beat)

        if self.is_scored:
            col = max(time_to_preview_col(self.target_time), 0)
            if col < len(PreviewData.note_counts_by_col):
                PreviewData.note_counts_by_col[col] += 1

    def render(self):
        if abs(self.lane) > 12:
            return
        if not self.is_scored:
            return
        draw_note(self.kind, self.lane, self.size, self.direction, self.target_time)

    @property
    def head_ease_frac(self) -> float:
        if self.is_attached:
            return unlerp_clamped(
                self.attach_head_ref.get().target_time, self.attach_tail_ref.get().target_time, self.target_time
            )
        else:
            return 0.0

    @property
    def tail_ease_frac(self) -> float:
        if self.is_attached:
            return unlerp_clamped(
                self.attach_head_ref.get().target_time, self.attach_tail_ref.get().target_time, self.target_time
            )
        else:
            return 1.0


def draw_note(kind: NoteKind, lane: float, size: float, direction: FlickDirection, target_time: float):
    col = time_to_preview_col(target_time)
    y = time_to_preview_y(target_time, col)
    sprite_set = get_note_sprite_set(kind, direction)
    draw_note_body(sprite_set.body, kind, lane, size, target_time, col, y)
    draw_note_arrow(sprite_set.arrow, lane, size, target_time, direction, col, y)
    draw_note_tick(sprite_set.tick, lane, target_time, col, y)


def draw_note_body(
    sprites: BodySpriteSet, kind: NoteKind, lane: float, size: float, target_time: float, col: int, y: float
):
    layer = get_note_body_layer(kind)
    z = get_z(layer, time=get_adjusted_time(target_time, col), lane=lane)
    match sprites.render_type:
        case BodyRenderType.NORMAL:
            left_layout, middle_layout, right_layout = layout_preview_regular_note_body(lane, size, col, y)
            sprites.left.draw(left_layout, z=z)
            sprites.middle.draw(middle_layout, z=z)
            sprites.right.draw(right_layout, z=z)
        case BodyRenderType.SLIM:
            left_layout, middle_layout, right_layout = layout_preview_slim_note_body(lane, size, col, y)
            sprites.left.draw(left_layout, z=z)
            sprites.middle.draw(middle_layout, z=z)
            sprites.right.draw(right_layout, z=z)
        case BodyRenderType.NORMAL_FALLBACK:
            layout = layout_preview_regular_note_body_fallback(lane, size, col, y)
            sprites.middle.draw(layout, z=z)
        case BodyRenderType.SLIM_FALLBACK:
            layout = layout_preview_slim_note_body_fallback(lane, size, col, y)
            sprites.middle.draw(layout, z=z)


def draw_note_arrow(
    sprites: ArrowSpriteSet, lane: float, size: float, target_time: float, direction: FlickDirection, col: int, y: float
):
    z = get_z(LAYER_NOTE_ARROW, time=get_adjusted_time(target_time, col), lane=lane)
    match sprites.render_type:
        case ArrowRenderType.NORMAL:
            layout = layout_preview_flick_arrow(lane, size, direction, col, y)
            sprites.get_sprite(size, direction).draw(layout, z=z)
        case ArrowRenderType.FALLBACK:
            layout = layout_preview_flick_arrow_fallback(lane, size, direction, col, y)
            sprites.get_sprite(size, direction).draw(layout, z=z)


def draw_note_tick(kind: NoteKind, lane: float, target_time: float, col: int, y: float):
    match kind:
        case NoteKind.NORM_TICK:
            _draw_tick(normal_tick_sprites, lane, target_time, col, y)
        case NoteKind.CRIT_TICK:
            _draw_tick(critical_tick_sprites, lane, target_time, col, y)
        case NoteKind.NORM_TRACE | NoteKind.NORM_HEAD_TRACE | NoteKind.NORM_TAIL_TRACE:
            _draw_tick(normal_trace_tick_sprites, lane, target_time, col, y)
        case (
            NoteKind.CRIT_TRACE
            | NoteKind.CRIT_HEAD_TRACE
            | NoteKind.CRIT_TAIL_TRACE
            | NoteKind.CRIT_TRACE_FLICK
            | NoteKind.CRIT_HEAD_TRACE_FLICK
            | NoteKind.CRIT_TAIL_TRACE_FLICK
        ):
            _draw_tick(critical_trace_tick_sprites, lane, target_time, col, y)
        case NoteKind.NORM_TRACE_FLICK | NoteKind.NORM_HEAD_TRACE_FLICK | NoteKind.NORM_TAIL_TRACE_FLICK:
            _draw_tick(trace_flick_tick_sprites, lane, target_time, col, y)
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


def _draw_regular_body(sprites: BodySprites, lane: float, size: float, target_time: float, col: int, y: float):
    z = get_z(LAYER_NOTE_BODY, time=target_time, lane=lane, current_time=col * PREVIEW_COLUMN_SECS)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_preview_regular_note_body(lane, size, col, y)
        sprites.left.draw(left_layout, z=z)
        sprites.middle.draw(middle_layout, z=z)
        sprites.right.draw(right_layout, z=z)
    else:
        layout = layout_preview_regular_note_body_fallback(lane, size, col, y)
        sprites.fallback.draw(layout, z=z)


def _draw_flick_body(sprites: BodySprites, lane: float, size: float, target_time: float, col: int, y: float):
    z = get_z(LAYER_NOTE_FLICK_BODY, time=target_time, lane=lane, current_time=col * PREVIEW_COLUMN_SECS)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_preview_regular_note_body(lane, size, col, y)
        sprites.left.draw(left_layout, z=z)
        sprites.middle.draw(middle_layout, z=z)
        sprites.right.draw(right_layout, z=z)
    else:
        layout = layout_preview_regular_note_body_fallback(lane, size, col, y)
        sprites.fallback.draw(layout, z=z)


def _draw_slim_body(sprites: BodySprites, lane: float, size: float, target_time: float, col: int, y: float):
    z = get_z(LAYER_NOTE_SLIM_BODY, time=target_time, lane=lane, current_time=col * PREVIEW_COLUMN_SECS)
    if sprites.custom_available:
        left_layout, middle_layout, right_layout = layout_preview_slim_note_body(lane, size, col, y)
        sprites.left.draw(left_layout, z=z)
        sprites.middle.draw(middle_layout, z=z)
        sprites.right.draw(right_layout, z=z)
    else:
        layout = layout_preview_slim_note_body_fallback(lane, size, col, y)
        sprites.fallback.draw(layout, z=z)


def _draw_tick(sprites: TickSprites, lane: float, target_time: float, col: int, y: float):
    z = get_z(LAYER_NOTE_TICK, time=target_time, lane=lane, current_time=col * PREVIEW_COLUMN_SECS)
    layout = layout_preview_tick(lane, col, y)
    if sprites.custom_available:
        sprites.normal.draw(layout, z=z)
    else:
        sprites.fallback.draw(layout, z=z)


def _draw_arrow(
    sprites: ArrowSprites, lane: float, size: float, target_time: float, direction: FlickDirection, col: int, y: float
):
    z = get_z(LAYER_NOTE_ARROW, time=target_time, lane=lane, current_time=col * PREVIEW_COLUMN_SECS)
    if sprites.custom_available:
        layout = layout_preview_flick_arrow(lane, size, direction, col, y)
        sprites.get_sprite(size, direction).draw(layout, z=z)
    else:
        layout = layout_preview_flick_arrow_fallback(lane, size, direction, col, y)
        sprites.fallback.draw(layout, z=z)


PREVIEW_NOTE_ARCHETYPES = derive_note_archetypes(PreviewBaseNote)
