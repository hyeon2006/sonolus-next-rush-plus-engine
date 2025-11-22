from __future__ import annotations

from enum import IntEnum
from typing import Self, assert_never

from sonolus.script.globals import level_data
from sonolus.script.interval import clamp
from sonolus.script.record import Record
from sonolus.script.sprite import Sprite, SpriteGroup, StandardSprite, skin, sprite, sprite_group

from sekai.lib.layout import FlickDirection


@skin
class BaseSkin:
    cover: StandardSprite.STAGE_COVER

    lane: StandardSprite.LANE
    judgment_line: StandardSprite.JUDGMENT_LINE
    stage_left_border: StandardSprite.STAGE_LEFT_BORDER
    stage_right_border: StandardSprite.STAGE_RIGHT_BORDER

    sekai_stage: Sprite = sprite("Sekai Stage")

    sim_line: StandardSprite.SIMULTANEOUS_CONNECTION_NEUTRAL

    note_cyan_left: Sprite = sprite("Sekai Note Cyan Left")
    note_cyan_middle: Sprite = sprite("Sekai Note Cyan Middle")
    note_cyan_right: Sprite = sprite("Sekai Note Cyan Right")
    note_cyan_fallback: StandardSprite.NOTE_HEAD_CYAN

    note_green_left: Sprite = sprite("Sekai Note Green Left")
    note_green_middle: Sprite = sprite("Sekai Note Green Middle")
    note_green_right: Sprite = sprite("Sekai Note Green Right")
    note_green_fallback: StandardSprite.NOTE_HEAD_GREEN

    note_red_left: Sprite = sprite("Sekai Note Red Left")
    note_red_middle: Sprite = sprite("Sekai Note Red Middle")
    note_red_right: Sprite = sprite("Sekai Note Red Right")
    note_red_fallback: StandardSprite.NOTE_HEAD_RED

    note_yellow_left: Sprite = sprite("Sekai Note Yellow Left")
    note_yellow_middle: Sprite = sprite("Sekai Note Yellow Middle")
    note_yellow_right: Sprite = sprite("Sekai Note Yellow Right")
    note_yellow_fallback: StandardSprite.NOTE_HEAD_YELLOW

    normal_note_left: Sprite = sprite("Sekai Normal Note Left")
    normal_note_middle: Sprite = sprite("Sekai Normal Note Middle")
    normal_note_right: Sprite = sprite("Sekai Normal Note Right")
    normal_note_basic: Sprite = sprite("Sekai Normal Note Basic")

    slide_note_left: Sprite = sprite("Sekai Slide Note Left")
    slide_note_middle: Sprite = sprite("Sekai Slide Note Middle")
    slide_note_right: Sprite = sprite("Sekai Slide Note Right")
    slide_note_basic: Sprite = sprite("Sekai Slide Note Basic")

    flick_note_left: Sprite = sprite("Sekai Flick Note Left")
    flick_note_middle: Sprite = sprite("Sekai Flick Note Middle")
    flick_note_right: Sprite = sprite("Sekai Flick Note Right")
    flick_note_basic: Sprite = sprite("Sekai Flick Note Basic")

    down_flick_note_left: Sprite = sprite("Sekai Down Flick Note Left")
    down_flick_note_middle: Sprite = sprite("Sekai Down Flick Note Middle")
    down_flick_note_right: Sprite = sprite("Sekai Down Flick Note Right")

    critical_note_left: Sprite = sprite("Sekai Critical Note Left")
    critical_note_middle: Sprite = sprite("Sekai Critical Note Middle")
    critical_note_right: Sprite = sprite("Sekai Critical Note Right")
    critical_note_basic: Sprite = sprite("Sekai Critical Note Basic")

    critical_slide_note_left: Sprite = sprite("Sekai Critical Slide Note Left")
    critical_slide_note_middle: Sprite = sprite("Sekai Critical Slide Note Middle")
    critical_slide_note_right: Sprite = sprite("Sekai Critical Slide Note Right")
    critical_slide_note_basic: Sprite = sprite("Sekai Critical Slide Note Basic")

    critical_flick_note_left: Sprite = sprite("Sekai Critical Flick Note Left")
    critical_flick_note_middle: Sprite = sprite("Sekai Critical Flick Note Middle")
    critical_flick_note_right: Sprite = sprite("Sekai Critical Flick Note Right")
    critical_flick_note_basic: Sprite = sprite("Sekai Critical Flick Note Basic")

    critical_down_flick_note_left: Sprite = sprite("Sekai Critical Down Flick Note Left")
    critical_down_flick_note_middle: Sprite = sprite("Sekai Critical Down Flick Note Middle")
    critical_down_flick_note_right: Sprite = sprite("Sekai Critical Down Flick Note Right")

    slide_tick_note_green: Sprite = sprite("Sekai Diamond Green")
    slide_tick_note_green_fallback: StandardSprite.NOTE_TICK_GREEN

    slide_tick_note_yellow: Sprite = sprite("Sekai Diamond Yellow")
    slide_tick_note_yellow_fallback: StandardSprite.NOTE_TICK_YELLOW

    normal_slide_tick_note: Sprite = sprite("Sekai Normal Slide Diamond")

    critical_slide_tick_note: Sprite = sprite("Sekai Critical Slide Diamond")

    active_slide_connection_green_normal: Sprite = sprite("Sekai Active Slide Connection Green")
    active_slide_connection_green_active: Sprite = sprite("Sekai Active Slide Connection Green Active")
    active_slide_connection_green_fallback: StandardSprite.NOTE_CONNECTION_GREEN_SEAMLESS

    active_slide_connection_yellow_normal: Sprite = sprite("Sekai Active Slide Connection Yellow")
    active_slide_connection_yellow_active: Sprite = sprite("Sekai Active Slide Connection Yellow Active")
    active_slide_connection_yellow_fallback: StandardSprite.NOTE_CONNECTION_YELLOW_SEAMLESS

    normal_active_slide_connection_normal: Sprite = sprite("Sekai Normal Active Slide Connection Normal")
    normal_active_slide_connection_active: Sprite = sprite("Sekai Normal Active Slide Connection Active")

    critical_active_slide_connection_normal: Sprite = sprite("Sekai Critical Active Slide Connection Normal")
    critical_active_slide_connection_active: Sprite = sprite("Sekai Critical Active Slide Connection Active")

    slot_cyan: Sprite = sprite("Sekai Slot Cyan")
    slot_green: Sprite = sprite("Sekai Slot Green")
    slot_red: Sprite = sprite("Sekai Slot Red")
    slot_yellow: Sprite = sprite("Sekai Slot Yellow")
    slot_yellow_flick: Sprite = sprite("Sekai Slot Yellow Flick")
    slot_yellow_slider: Sprite = sprite("Sekai Slot Yellow Slider")

    slot_normal: Sprite = sprite("Sekai Slot Normal")
    slot_slide: Sprite = sprite("Sekai Slot Slide")
    slot_flick: Sprite = sprite("Sekai Slot Flick")
    slot_down_flick: Sprite = sprite("Sekai Slot Down Flick")
    slot_critical: Sprite = sprite("Sekai Slot Critical")
    slot_critical_slide: Sprite = sprite("Sekai Slot Critical Slide")
    slot_critical_flick: Sprite = sprite("Sekai Slot Critical Flick")
    slot_critical_down_flick: Sprite = sprite("Sekai Slot Critical Down Flick")

    slot_glow_cyan: Sprite = sprite("Sekai Slot Glow Cyan")
    slot_glow_green: Sprite = sprite("Sekai Slot Glow Green")
    slot_glow_red: Sprite = sprite("Sekai Slot Glow Red")
    slot_glow_yellow: Sprite = sprite("Sekai Slot Glow Yellow")
    slot_glow_yellow_flick: Sprite = sprite("Sekai Slot Glow Yellow Flick")
    slot_glow_yellow_slider_tap: Sprite = sprite("Sekai Slot Glow Yellow Slider Tap")

    slot_glow_normal: Sprite = sprite("Sekai Slot Glow Normal")
    slot_glow_slide: Sprite = sprite("Sekai Slot Glow Slide")
    slot_glow_flick: Sprite = sprite("Sekai Slot Glow Flick")
    slot_glow_down_flick: Sprite = sprite("Sekai Slot Glow Down Flick")
    slot_glow_critical: Sprite = sprite("Sekai Slot Glow Critical")
    slot_glow_critical_slide: Sprite = sprite("Sekai Slot Glow Critical Slide")
    slot_glow_critical_flick: Sprite = sprite("Sekai Slot Glow Critical Flick")
    slot_glow_critical_down_flick: Sprite = sprite("Sekai Slot Glow Critical Down Flick")

    slide_connector_slot_glow_green: Sprite = sprite("Sekai Slot Glow Green Slider Hold")
    slide_connector_slot_glow_yellow: Sprite = sprite("Sekai Slot Glow Yellow Slider Hold")

    normal_slide_connector_slot_glow: Sprite = sprite("Sekai Normal Slide Slot Glow")
    critical_slide_connector_slot_glow: Sprite = sprite("Sekai Critical Slide Slot Glow")

    flick_arrow_red_up: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Up {i}" for i in range(1, 7))
    flick_arrow_red_up_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Up Left {i}" for i in range(1, 7))
    flick_arrow_red_down: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Down {i}" for i in range(1, 7))
    flick_arrow_red_down_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Down Left {i}" for i in range(1, 7))
    flick_arrow_red_fallback: StandardSprite.DIRECTIONAL_MARKER_RED

    flick_arrow_yellow_up: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Up {i}" for i in range(1, 7))
    flick_arrow_yellow_up_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Up Left {i}" for i in range(1, 7))
    flick_arrow_yellow_down: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Down {i}" for i in range(1, 7))
    flick_arrow_yellow_down_left: SpriteGroup = sprite_group(
        f"Sekai Flick Arrow Yellow Down Left {i}" for i in range(1, 7)
    )
    flick_arrow_yellow_fallback: StandardSprite.DIRECTIONAL_MARKER_YELLOW

    flick_arrow_up: SpriteGroup = sprite_group(f"Sekai Flick Arrow Up {i}" for i in range(1, 7))
    flick_arrow_up_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Up Left {i}" for i in range(1, 7))
    flick_arrow_down: SpriteGroup = sprite_group(f"Sekai Flick Arrow Down {i}" for i in range(1, 7))
    flick_arrow_down_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Down Left {i}" for i in range(1, 7))

    critical_flick_arrow_up: SpriteGroup = sprite_group(f"Sekai Critical Flick Arrow Up {i}" for i in range(1, 7))
    critical_flick_arrow_up_left: SpriteGroup = sprite_group(
        f"Sekai Critical Flick Arrow Up Left {i}" for i in range(1, 7)
    )
    critical_flick_arrow_down: SpriteGroup = sprite_group(f"Sekai Critical Flick Arrow Down {i}" for i in range(1, 7))
    critical_flick_arrow_down_left: SpriteGroup = sprite_group(
        f"Sekai Critical Flick Arrow Down Left {i}" for i in range(1, 7)
    )

    trace_note_green_left: Sprite = sprite("Sekai Trace Note Green Left")
    trace_note_green_middle: Sprite = sprite("Sekai Trace Note Green Middle")
    trace_note_green_right: Sprite = sprite("Sekai Trace Note Green Right")
    trace_note_green_fallback: StandardSprite.NOTE_HEAD_GREEN
    trace_note_green_tick: Sprite = sprite("Sekai Trace Diamond Green")
    trace_note_green_tick_fallback: StandardSprite.NOTE_TICK_GREEN

    trace_note_red_left: Sprite = sprite("Sekai Trace Note Red Left")
    trace_note_red_middle: Sprite = sprite("Sekai Trace Note Red Middle")
    trace_note_red_right: Sprite = sprite("Sekai Trace Note Red Right")
    trace_note_red_fallback: StandardSprite.NOTE_HEAD_RED
    trace_note_red_tick: Sprite = sprite("Sekai Trace Diamond Red")
    trace_note_red_tick_fallback: StandardSprite.NOTE_TICK_RED

    trace_note_yellow_left: Sprite = sprite("Sekai Trace Note Yellow Left")
    trace_note_yellow_middle: Sprite = sprite("Sekai Trace Note Yellow Middle")
    trace_note_yellow_right: Sprite = sprite("Sekai Trace Note Yellow Right")
    trace_note_yellow_fallback: StandardSprite.NOTE_HEAD_YELLOW
    trace_note_yellow_tick: Sprite = sprite("Sekai Trace Diamond Yellow")
    trace_note_yellow_tick_fallback: StandardSprite.NOTE_TICK_YELLOW

    trace_note_purple_left: Sprite = sprite("Sekai Trace Note Purple Left")
    trace_note_purple_middle: Sprite = sprite("Sekai Trace Note Purple Middle")
    trace_note_purple_right: Sprite = sprite("Sekai Trace Note Purple Right")
    trace_note_purple_fallback: StandardSprite.NOTE_HEAD_PURPLE

    normal_trace_note_left: Sprite = sprite("Sekai Normal Trace Note Left")
    normal_trace_note_middle: Sprite = sprite("Sekai Normal Trace Note Middle")
    normal_trace_note_right: Sprite = sprite("Sekai Normal Trace Note Right")
    normal_trace_note_tick: Sprite = sprite("Sekai Normal Trace Diamond")
    normal_trace_note_basic: Sprite = sprite("Sekai Normal Trace Note Basic")

    trace_flick_note_left: Sprite = sprite("Sekai Trace Flick Note Left")
    trace_flick_note_middle: Sprite = sprite("Sekai Trace Flick Note Middle")
    trace_flick_note_right: Sprite = sprite("Sekai Trace Flick Note Right")
    trace_flick_note_tick: Sprite = sprite("Sekai Trace Flick Diamond")
    trace_flick_note_basic: Sprite = sprite("Sekai Trace Flick Note Basic")

    trace_down_flick_note_left: Sprite = sprite("Sekai Trace Down Flick Note Left")
    trace_down_flick_note_middle: Sprite = sprite("Sekai Trace Down Flick Note Middle")
    trace_down_flick_note_right: Sprite = sprite("Sekai Trace Down Flick Note Right")
    trace_down_flick_note_tick: Sprite = sprite("Sekai Trace Down Flick Diamond")

    critical_trace_note_left: Sprite = sprite("Sekai Critical Trace Note Left")
    critical_trace_note_middle: Sprite = sprite("Sekai Critical Trace Note Middle")
    critical_trace_note_right: Sprite = sprite("Sekai Critical Trace Note Right")
    critical_trace_note_tick: Sprite = sprite("Sekai Critical Trace Diamond")
    critical_trace_note_basic: Sprite = sprite("Sekai Critical Trace Note Basic")

    critical_trace_flick_note_left: Sprite = sprite("Sekai Critical Trace Flick Note Left")
    critical_trace_flick_note_middle: Sprite = sprite("Sekai Critical Trace Flick Note Middle")
    critical_trace_flick_note_right: Sprite = sprite("Sekai Critical Trace Flick Note Right")
    critical_trace_flick_note_tick: Sprite = sprite("Sekai Critical Trace Flick Diamond")
    critical_trace_flick_note_basic: Sprite = sprite("Sekai Critical Trace Flick Note Basic")

    critical_trace_down_flick_note_left: Sprite = sprite("Sekai Critical Trace Down Flick Note Left")
    critical_trace_down_flick_note_middle: Sprite = sprite("Sekai Critical Trace Down Flick Note Middle")
    critical_trace_down_flick_note_right: Sprite = sprite("Sekai Critical Trace Down Flick Note Right")
    critical_trace_down_flick_note_tick: Sprite = sprite("Sekai Critical Trace Down Flick Diamond")

    damage_note_left: Sprite = sprite("Sekai Damage Note Left")
    damage_note_middle: Sprite = sprite("Sekai Damage Note Middle")
    damage_note_right: Sprite = sprite("Sekai Damage Note Right")
    damage_note_basic: Sprite = sprite("Sekai Damage Note Basic")

    guide_green: Sprite = sprite("Sekai Guide Green")
    guide_green_fallback: StandardSprite.NOTE_CONNECTION_GREEN_SEAMLESS
    guide_yellow: Sprite = sprite("Sekai Guide Yellow")
    guide_yellow_fallback: StandardSprite.NOTE_CONNECTION_YELLOW_SEAMLESS
    guide_red: Sprite = sprite("Sekai Guide Red")
    guide_red_fallback: StandardSprite.NOTE_CONNECTION_RED_SEAMLESS
    guide_purple: Sprite = sprite("Sekai Guide Purple")
    guide_purple_fallback: StandardSprite.NOTE_CONNECTION_PURPLE_SEAMLESS
    guide_cyan: Sprite = sprite("Sekai Guide Cyan")
    guide_cyan_fallback: StandardSprite.NOTE_CONNECTION_CYAN_SEAMLESS
    guide_blue: Sprite = sprite("Sekai Guide Blue")
    guide_blue_fallback: StandardSprite.NOTE_CONNECTION_BLUE_SEAMLESS
    guide_neutral: Sprite = sprite("Sekai Guide Neutral")
    guide_neutral_fallback: StandardSprite.NOTE_CONNECTION_NEUTRAL_SEAMLESS
    guide_black: Sprite = sprite("Sekai Guide Black")
    guide_black_fallback: StandardSprite.NOTE_CONNECTION_NEUTRAL_SEAMLESS

    beat_line: StandardSprite.GRID_NEUTRAL
    bpm_change_line: StandardSprite.GRID_PURPLE
    timescale_change_line: StandardSprite.GRID_YELLOW
    special_line: StandardSprite.GRID_RED


# class BodySprites(Record):
#     left: Sprite
#     middle: Sprite
#     right: Sprite
#     fallback: Sprite
#
#     @property
#     def custom_available(self):
#         return self.left.is_available
#
#
# class ArrowSprites(Record):
#     up: SpriteGroup
#     up_left: SpriteGroup
#     down: SpriteGroup
#     down_left: SpriteGroup
#     fallback: Sprite
#
#     def _get_index_from_size(self, size: float) -> int:
#         return int(clamp(round(size * 2), 1, 6)) - 1
#
#     def get_sprite(self, size: float, direction: FlickDirection) -> Sprite:
#         result = +Sprite
#         index = self._get_index_from_size(size)
#         match direction:
#             case FlickDirection.UP_OMNI:
#                 result @= self.up[index]
#             case FlickDirection.DOWN_OMNI:
#                 result @= self.down[index]
#             case FlickDirection.UP_LEFT | FlickDirection.UP_RIGHT:
#                 result @= self.up_left[index]
#             case FlickDirection.DOWN_LEFT | FlickDirection.DOWN_RIGHT:
#                 result @= self.down_left[index]
#             case _:
#                 assert_never(direction)
#         return result
#
#     @property
#     def custom_available(self):
#         return self.up_left[0].is_available
#
#
# class TickSprites(Record):
#     normal: Sprite
#     fallback: Sprite
#
#     @property
#     def custom_available(self):
#         return self.normal.is_available
#
#
# class ActiveConnectorSprites(Record):
#     normal: Sprite
#     active: Sprite
#     fallback: Sprite
#
#     @property
#     def custom_available(self):
#         return self.normal.is_available
#
#
# class GuideSprites(Record):
#     normal: Sprite
#     fallback: Sprite
#
#     @property
#     def custom_available(self):
#         return self.normal.is_available


# normal_note_body_sprites = BodySprites(
#     left=BaseSkin.normal_note_left,
#     middle=BaseSkin.normal_note_middle,
#     right=BaseSkin.normal_note_right,
#     fallback=BaseSkin.normal_note_fallback,
# )
# slide_note_body_sprites = BodySprites(
#     left=BaseSkin.slide_note_left,
#     middle=BaseSkin.slide_note_middle,
#     right=BaseSkin.slide_note_right,
#     fallback=BaseSkin.slide_note_fallback,
# )
# flick_note_body_sprites = BodySprites(
#     left=BaseSkin.flick_note_left,
#     middle=BaseSkin.flick_note_middle,
#     right=BaseSkin.flick_note_right,
#     fallback=BaseSkin.flick_note_fallback,
# )
# critical_note_body_sprites = BodySprites(
#     left=BaseSkin.critical_note_left,
#     middle=BaseSkin.critical_note_middle,
#     right=BaseSkin.critical_note_right,
#     fallback=BaseSkin.critical_note_fallback,
# )
#
# normal_trace_note_body_sprites = BodySprites(
#     left=BaseSkin.normal_trace_note_left,
#     middle=BaseSkin.normal_trace_note_middle,
#     right=BaseSkin.normal_trace_note_right,
#     fallback=BaseSkin.normal_trace_note_fallback,
# )
# critical_trace_note_body_sprites = BodySprites(
#     left=BaseSkin.critical_trace_note_left,
#     middle=BaseSkin.critical_trace_note_middle,
#     right=BaseSkin.critical_trace_note_right,
#     fallback=BaseSkin.critical_trace_note_fallback,
# )
# trace_flick_note_body_sprites = BodySprites(
#     left=BaseSkin.trace_flick_note_left,
#     middle=BaseSkin.trace_flick_note_middle,
#     right=BaseSkin.trace_flick_note_right,
#     fallback=BaseSkin.trace_flick_note_fallback,
# )
# trace_slide_note_body_sprites = normal_trace_note_body_sprites
#
# damage_note_body_sprites = BodySprites(
#     left=BaseSkin.damage_note_left,
#     middle=BaseSkin.damage_note_middle,
#     right=BaseSkin.damage_note_right,
#     fallback=BaseSkin.damage_note_fallback,
# )
#
# normal_arrow_sprites = ArrowSprites(
#     up=BaseSkin.flick_arrow_up,
#     up_left=BaseSkin.flick_arrow_up_left,
#     down=BaseSkin.flick_arrow_down,
#     down_left=BaseSkin.flick_arrow_down_left,
#     fallback=BaseSkin.flick_arrow_fallback,
# )
# critical_arrow_sprites = ArrowSprites(
#     up=BaseSkin.critical_arrow_up,
#     up_left=BaseSkin.critical_arrow_up_left,
#     down=BaseSkin.critical_arrow_down,
#     down_left=BaseSkin.critical_arrow_down_left,
#     fallback=BaseSkin.critical_arrow_fallback,
# )
#
# normal_tick_sprites = TickSprites(
#     normal=BaseSkin.normal_slide_tick_note,
#     fallback=BaseSkin.normal_slide_tick_note_fallback,
# )
# slide_tick_sprites = normal_tick_sprites
# critical_tick_sprites = TickSprites(
#     normal=BaseSkin.critical_slide_tick_note,
#     fallback=BaseSkin.critical_slide_tick_note_fallback,
# )
# normal_trace_tick_sprites = TickSprites(
#     normal=BaseSkin.normal_trace_tick_note,
#     fallback=BaseSkin.normal_trace_tick_note_fallback,
# )
# critical_trace_tick_sprites = TickSprites(
#     normal=BaseSkin.critical_trace_tick_note,
#     fallback=BaseSkin.critical_trace_tick_note_fallback,
# )
# trace_flick_tick_sprites = TickSprites(
#     normal=BaseSkin.trace_flick_tick_note,
#     fallback=BaseSkin.trace_flick_tick_note_fallback,
# )
#
# normal_slide_connector_sprites = ActiveConnectorSprites(
#     normal=BaseSkin.normal_slide_connector_normal,
#     active=BaseSkin.normal_slide_connector_active,
#     fallback=BaseSkin.normal_slide_connector_fallback,
# )
# critical_slide_connector_sprites = ActiveConnectorSprites(
#     normal=BaseSkin.critical_slide_connector_normal,
#     active=BaseSkin.critical_slide_connector_active,
#     fallback=BaseSkin.critical_slide_connector_fallback,
# )
#
# neutral_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_neutral,
#     fallback=BaseSkin.guide_neutral_fallback,
# )
# red_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_red,
#     fallback=BaseSkin.guide_red_fallback,
# )
# green_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_green,
#     fallback=BaseSkin.guide_green_fallback,
# )
# blue_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_blue,
#     fallback=BaseSkin.guide_blue_fallback,
# )
# yellow_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_yellow,
#     fallback=BaseSkin.guide_yellow_fallback,
# )
# purple_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_purple,
#     fallback=BaseSkin.guide_purple_fallback,
# )
# cyan_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_cyan,
#     fallback=BaseSkin.guide_cyan_fallback,
# )
# black_guide_sprites = GuideSprites(
#     normal=BaseSkin.guide_black,
#     fallback=BaseSkin.guide_black_fallback,
# )

EMPTY_SPRITE = Sprite(-1)
EMPTY_SPRITE_GROUP = SpriteGroup(-1, 1)


def first_available_sprite(*sprites: Sprite) -> Sprite:
    result = +EMPTY_SPRITE
    for s in sprites:
        if s.is_available:
            result @= s
            break
    return result


def first_available_sprite_group(*groups: SpriteGroup) -> SpriteGroup:
    result = +EMPTY_SPRITE_GROUP
    for g in groups:
        if g[0].is_available:
            result @= g
            break
    return result


class BodyRenderType(IntEnum):
    NORMAL = 0
    SLIM = 1
    NORMAL_FALLBACK = 2
    SLIM_FALLBACK = 3


class BodySpriteSet(Record):
    render_type: BodyRenderType
    left: Sprite
    middle: Sprite
    right: Sprite

    @property
    def available(self):
        return self.middle.is_available

    @classmethod
    def of_normal(cls, left: Sprite, middle: Sprite, right: Sprite) -> Self:
        return cls(
            render_type=BodyRenderType.NORMAL,
            left=left,
            middle=middle,
            right=right,
        )

    @classmethod
    def of_slim(cls, left: Sprite, middle: Sprite, right: Sprite) -> Self:
        return cls(
            render_type=BodyRenderType.SLIM,
            left=left,
            middle=middle,
            right=right,
        )

    @classmethod
    def of_normal_fallback(cls, fallback: Sprite) -> Self:
        return cls(
            render_type=BodyRenderType.NORMAL_FALLBACK,
            left=EMPTY_SPRITE,
            middle=fallback,
            right=EMPTY_SPRITE,
        )

    @classmethod
    def of_slim_fallback(cls, fallback: Sprite) -> Self:
        return cls(
            render_type=BodyRenderType.SLIM_FALLBACK,
            left=EMPTY_SPRITE,
            middle=fallback,
            right=EMPTY_SPRITE,
        )


EMPTY_BODY_SPRITE_SET = BodySpriteSet(
    render_type=BodyRenderType.NORMAL_FALLBACK,
    left=EMPTY_SPRITE,
    middle=EMPTY_SPRITE,
    right=EMPTY_SPRITE,
)


def first_available_body_sprite_set(*sets: BodySpriteSet) -> BodySpriteSet:
    result = +EMPTY_BODY_SPRITE_SET
    for s in sets:
        if s.available:
            result @= s
            break
    return result


class ArrowRenderType(IntEnum):
    NORMAL = 0
    FALLBACK = 1


class ArrowSpriteSet(Record):
    render_type: ArrowRenderType
    up: SpriteGroup
    up_left: SpriteGroup
    down: SpriteGroup
    down_left: SpriteGroup

    def _get_index_from_size(self, size: float) -> int:
        return int(clamp(round(size * 2), 1, 6)) - 1

    def get_sprite(self, size: float, direction) -> Sprite:
        result = +Sprite
        match self.render_type:
            case ArrowRenderType.NORMAL:
                index = self._get_index_from_size(size)
                match direction:
                    case FlickDirection.UP_OMNI:
                        result @= self.up[index]
                    case FlickDirection.DOWN_OMNI:
                        result @= self.down[index]
                    case FlickDirection.UP_LEFT | FlickDirection.UP_RIGHT:
                        result @= self.up_left[index]
                    case FlickDirection.DOWN_LEFT | FlickDirection.DOWN_RIGHT:
                        result @= self.down_left[index]
                    case _:
                        assert_never(direction)
            case ArrowRenderType.FALLBACK:
                result @= self.up[0]
            case _:
                assert_never(self.render_type)
        return result

    @property
    def available(self):
        return self.up[0].is_available

    @classmethod
    def of_normal(cls, up: SpriteGroup, up_left: SpriteGroup, down: SpriteGroup, down_left: SpriteGroup) -> Self:
        return cls(
            render_type=ArrowRenderType.NORMAL,
            up=up,
            up_left=up_left,
            down=down,
            down_left=down_left,
        )

    @classmethod
    def of_fallback(cls, fallback: Sprite) -> Self:
        return cls(
            render_type=ArrowRenderType.FALLBACK,
            up=SpriteGroup(fallback.id, 1),
            up_left=EMPTY_SPRITE_GROUP,
            down=EMPTY_SPRITE_GROUP,
            down_left=EMPTY_SPRITE_GROUP,
        )


def first_available_arrow_sprite_set(*sets: ArrowSpriteSet) -> ArrowSpriteSet:
    result = +EMPTY_ARROW_SPRITE_SET
    for s in sets:
        if s.available:
            result @= s
            break
    return result


EMPTY_ARROW_SPRITE_SET = ArrowSpriteSet(
    render_type=ArrowRenderType.FALLBACK,
    up=EMPTY_SPRITE_GROUP,
    up_left=EMPTY_SPRITE_GROUP,
    down=EMPTY_SPRITE_GROUP,
    down_left=EMPTY_SPRITE_GROUP,
)


class NoteSpriteSet(Record):
    body: BodySpriteSet
    arrow: ArrowSpriteSet
    tick: Sprite
    slot: Sprite
    slot_glow: Sprite


EMPTY_NOTE_SPRITE_SET = NoteSpriteSet(
    body=EMPTY_BODY_SPRITE_SET,
    arrow=EMPTY_ARROW_SPRITE_SET,
    tick=EMPTY_SPRITE,
    slot=EMPTY_SPRITE,
    slot_glow=EMPTY_SPRITE,
)


class ActiveConnectorRenderType(IntEnum):
    NORMAL = 0
    FALLBACK = 1


class ActiveConnectionSpriteSet(Record):
    render_type: ActiveConnectorRenderType
    normal: Sprite
    active: Sprite

    @property
    def available(self):
        return self.normal.is_available

    @classmethod
    def of_normal(cls, normal: Sprite, active: Sprite) -> Self:
        return cls(
            render_type=ActiveConnectorRenderType.NORMAL,
            normal=normal,
            active=active,
        )

    @classmethod
    def of_fallback(cls, fallback: Sprite) -> Self:
        return cls(
            render_type=ActiveConnectorRenderType.FALLBACK,
            normal=fallback,
            active=fallback,
        )


EMPTY_ACTIVE_CONNECTION_SPRITE_SET = ActiveConnectionSpriteSet(
    render_type=ActiveConnectorRenderType.FALLBACK,
    normal=EMPTY_SPRITE,
    active=EMPTY_SPRITE,
)


def first_available_active_connection_sprite_set(*sets: ActiveConnectionSpriteSet) -> ActiveConnectionSpriteSet:
    result = +EMPTY_ACTIVE_CONNECTION_SPRITE_SET
    for s in sets:
        if s.available:
            result @= s
            break
    return result


class ActiveConnectorSpriteSet(Record):
    connection: ActiveConnectionSpriteSet
    slot_glow: Sprite


note_cyan_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.note_cyan_left,
    middle=BaseSkin.note_cyan_middle,
    right=BaseSkin.note_cyan_right,
)
note_cyan_fallback_body_sprites = BodySpriteSet.of_normal_fallback(
    fallback=BaseSkin.note_cyan_fallback,
)
note_green_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.note_green_left,
    middle=BaseSkin.note_green_middle,
    right=BaseSkin.note_green_right,
)
note_green_fallback_body_sprites = BodySpriteSet.of_normal_fallback(
    fallback=BaseSkin.note_green_fallback,
)
note_red_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.note_red_left,
    middle=BaseSkin.note_red_middle,
    right=BaseSkin.note_red_right,
)
note_red_fallback_body_sprites = BodySpriteSet.of_normal_fallback(
    fallback=BaseSkin.note_red_fallback,
)
note_yellow_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.note_yellow_left,
    middle=BaseSkin.note_yellow_middle,
    right=BaseSkin.note_yellow_right,
)
note_yellow_fallback_body_sprites = BodySpriteSet.of_normal_fallback(
    fallback=BaseSkin.note_yellow_fallback,
)
normal_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.normal_note_left,
    middle=BaseSkin.normal_note_middle,
    right=BaseSkin.normal_note_right,
)
slide_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.slide_note_left,
    middle=BaseSkin.slide_note_middle,
    right=BaseSkin.slide_note_right,
)
flick_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.flick_note_left,
    middle=BaseSkin.flick_note_middle,
    right=BaseSkin.flick_note_right,
)
down_flick_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.down_flick_note_left,
    middle=BaseSkin.down_flick_note_middle,
    right=BaseSkin.down_flick_note_right,
)
critical_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.critical_note_left,
    middle=BaseSkin.critical_note_middle,
    right=BaseSkin.critical_note_right,
)
critical_slide_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.critical_slide_note_left,
    middle=BaseSkin.critical_slide_note_middle,
    right=BaseSkin.critical_slide_note_right,
)
critical_flick_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.critical_flick_note_left,
    middle=BaseSkin.critical_flick_note_middle,
    right=BaseSkin.critical_flick_note_right,
)
critical_down_flick_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.critical_down_flick_note_left,
    middle=BaseSkin.critical_down_flick_note_middle,
    right=BaseSkin.critical_down_flick_note_right,
)

flick_arrow_red_sprites = ArrowSpriteSet.of_normal(
    up=BaseSkin.flick_arrow_red_up,
    up_left=BaseSkin.flick_arrow_red_up_left,
    down=BaseSkin.flick_arrow_red_down,
    down_left=BaseSkin.flick_arrow_red_down_left,
)
flick_arrow_red_fallback_sprites = ArrowSpriteSet.of_fallback(
    fallback=BaseSkin.flick_arrow_red_fallback,
)
flick_arrow_yellow_sprites = ArrowSpriteSet.of_normal(
    up=BaseSkin.flick_arrow_yellow_up,
    up_left=BaseSkin.flick_arrow_yellow_up_left,
    down=BaseSkin.flick_arrow_yellow_down,
    down_left=BaseSkin.flick_arrow_yellow_down_left,
)
flick_arrow_yellow_fallback_sprites = ArrowSpriteSet.of_fallback(
    fallback=BaseSkin.flick_arrow_yellow_fallback,
)
flick_arrow_sprites = ArrowSpriteSet.of_normal(
    up=BaseSkin.flick_arrow_up,
    up_left=BaseSkin.flick_arrow_up_left,
    down=BaseSkin.flick_arrow_down,
    down_left=BaseSkin.flick_arrow_down_left,
)
critical_flick_arrow_sprites = ArrowSpriteSet.of_normal(
    up=BaseSkin.critical_flick_arrow_up,
    up_left=BaseSkin.critical_flick_arrow_up_left,
    down=BaseSkin.critical_flick_arrow_down,
    down_left=BaseSkin.critical_flick_arrow_down_left,
)

trace_note_green_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_note_green_left,
    middle=BaseSkin.trace_note_green_middle,
    right=BaseSkin.trace_note_green_right,
)
trace_note_green_fallback_body_sprites = BodySpriteSet.of_slim_fallback(
    fallback=BaseSkin.trace_note_green_fallback,
)
trace_note_red_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_note_red_left,
    middle=BaseSkin.trace_note_red_middle,
    right=BaseSkin.trace_note_red_right,
)
trace_note_red_fallback_body_sprites = BodySpriteSet.of_slim_fallback(
    fallback=BaseSkin.trace_note_red_fallback,
)
trace_note_yellow_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_note_yellow_left,
    middle=BaseSkin.trace_note_yellow_middle,
    right=BaseSkin.trace_note_yellow_right,
)
trace_note_yellow_fallback_body_sprites = BodySpriteSet.of_slim_fallback(
    fallback=BaseSkin.trace_note_yellow_fallback,
)
trace_note_purple_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_note_purple_left,
    middle=BaseSkin.trace_note_purple_middle,
    right=BaseSkin.trace_note_purple_right,
)
trace_note_purple_fallback_body_sprites = BodySpriteSet.of_slim_fallback(
    fallback=BaseSkin.trace_note_purple_fallback,
)
normal_trace_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.normal_trace_note_left,
    middle=BaseSkin.normal_trace_note_middle,
    right=BaseSkin.normal_trace_note_right,
)
trace_flick_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_flick_note_left,
    middle=BaseSkin.trace_flick_note_middle,
    right=BaseSkin.trace_flick_note_right,
)
trace_down_flick_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.trace_down_flick_note_left,
    middle=BaseSkin.trace_down_flick_note_middle,
    right=BaseSkin.trace_down_flick_note_right,
)
critical_trace_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.critical_trace_note_left,
    middle=BaseSkin.critical_trace_note_middle,
    right=BaseSkin.critical_trace_note_right,
)
critical_trace_flick_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.critical_trace_flick_note_left,
    middle=BaseSkin.critical_trace_flick_note_middle,
    right=BaseSkin.critical_trace_flick_note_right,
)
critical_trace_down_flick_note_body_sprites = BodySpriteSet.of_slim(
    left=BaseSkin.critical_trace_down_flick_note_left,
    middle=BaseSkin.critical_trace_down_flick_note_middle,
    right=BaseSkin.critical_trace_down_flick_note_right,
)
damage_note_body_sprites = BodySpriteSet.of_normal(
    left=BaseSkin.damage_note_left,
    middle=BaseSkin.damage_note_middle,
    right=BaseSkin.damage_note_right,
)

active_slide_connector_green_sprites = ActiveConnectionSpriteSet.of_normal(
    normal=BaseSkin.active_slide_connection_green_normal,
    active=BaseSkin.active_slide_connection_green_active,
)
active_slide_connector_green_fallback_sprites = ActiveConnectionSpriteSet.of_fallback(
    fallback=BaseSkin.active_slide_connection_green_fallback,
)
active_slide_connector_yellow_sprites = ActiveConnectionSpriteSet.of_normal(
    normal=BaseSkin.active_slide_connection_yellow_normal,
    active=BaseSkin.active_slide_connection_yellow_active,
)
active_slide_connector_yellow_fallback_sprites = ActiveConnectionSpriteSet.of_fallback(
    fallback=BaseSkin.active_slide_connection_yellow_fallback,
)
normal_active_slide_connector_sprites = ActiveConnectionSpriteSet.of_normal(
    normal=BaseSkin.normal_active_slide_connection_normal,
    active=BaseSkin.normal_active_slide_connection_active,
)
critical_active_slide_connector_sprites = ActiveConnectionSpriteSet.of_normal(
    normal=BaseSkin.critical_active_slide_connection_normal,
    active=BaseSkin.critical_active_slide_connection_active,
)

# normal_note_body_sprite_candidates = (
#     normal_note_body_sprites,
#     note_cyan_body_sprites,
#     note_cyan_fallback_body_sprites,
# )
# slide_note_body_sprite_candidates = (
#     slide_note_body_sprites,
#     note_green_body_sprites,
#     note_green_fallback_body_sprites,
# )
# flick_note_body_sprite_candidates = (
#     flick_note_body_sprites,
#     note_red_body_sprites,
#     note_red_fallback_body_sprites,
# )
# down_flick_note_body_sprite_candidates = (
#     down_flick_note_body_sprites,
#     flick_note_body_sprites,
#     note_red_body_sprites,
#     note_red_fallback_body_sprites,
# )
# critical_note_body_sprite_candidates = (
#     critical_note_body_sprites,
#     note_yellow_body_sprites,
#     note_yellow_fallback_body_sprites,
# )
# critical_slide_note_body_sprite_candidates = (
#     critical_slide_note_body_sprites,
#     critical_note_body_sprites,
#     note_yellow_body_sprites,
#     note_yellow_fallback_body_sprites,
# )
# critical_flick_note_body_sprite_candidates = (
#     critical_flick_note_body_sprites,
#     critical_note_body_sprites,
#     note_yellow_body_sprites,
#     note_yellow_fallback_body_sprites,
# )
# critical_down_flick_note_body_sprite_candidates = (
#     critical_down_flick_note_body_sprites,
#     critical_flick_note_body_sprites,
#     critical_note_body_sprites,
#     note_yellow_body_sprites,
#     note_yellow_fallback_body_sprites,
# )
#
# flick_note_arrow_sprite_candidates = (
#     flick_arrow_sprites,
#     flick_arrow_red_sprites,
#     flick_arrow_red_fallback_sprites,
# )
# critical_flick_note_arrow_sprite_candidates = (
#     critical_flick_arrow_sprites,
#     flick_arrow_red_sprites,
#     flick_arrow_red_fallback_sprites,
# )
#
# normal_slide_tick_sprite_candidates = (
#     BaseSkin.normal_slide_tick_note,
#     BaseSkin.normal_slide_tick_note_fallback,
# )
#
# critical_slide_tick_sprite_candidates = (
#     BaseSkin.critical_slide_tick_note,
#     BaseSkin.critical_slide_tick_note_fallback,
# )
#
# normal_trace_note_body_sprite_candidates = (
#     normal_trace_note_body_sprites,
#     trace_note_green_body_sprites,
#     trace_note_green_fallback_body_sprites,
# )
# trace_flick_note_body_sprite_candidates = (
#     trace_flick_note_body_sprites,
#     trace_note_red_body_sprites,
#     trace_note_red_fallback_body_sprites,
# )
# trace_down_flick_note_body_sprite_candidates = (
#     trace_down_flick_note_body_sprites,
#     trace_flick_note_body_sprites,
#     trace_note_red_body_sprites,
#     trace_note_red_fallback_body_sprites,
# )
# critical_trace_note_body_sprite_candidates = (
#     critical_trace_note_body_sprites,
#     trace_note_yellow_body_sprites,
#     trace_note_yellow_fallback_body_sprites,
# )
# critical_trace_flick_note_body_sprite_candidates = (
#     critical_trace_flick_note_body_sprites,
#     critical_trace_note_body_sprites,
#     trace_note_yellow_body_sprites,
#     trace_note_yellow_fallback_body_sprites,
# )
# critical_trace_down_flick_note_body_sprite_candidates = (
#     critical_trace_down_flick_note_body_sprites,
#     critical_trace_flick_note_body_sprites,
#     critical_trace_note_body_sprites,
#     trace_note_yellow_body_sprites,
#     trace_note_yellow_fallback_body_sprites,
# )
#
# normal_trace_tick_sprite_candidates = (
#     BaseSkin.normal_trace_note_tick,
#     BaseSkin.trace_note_green_tick,
#     BaseSkin.trace_note_green_tick_fallback,
# )
# trace_flick_tick_sprite_candidates = (
#     BaseSkin.trace_flick_note_tick,
#     BaseSkin.trace_note_red_tick,
#     BaseSkin.trace_note_red_tick_fallback,
# )
# trace_down_flick_tick_sprite_candidates = (
#     BaseSkin.trace_down_flick_note_tick,
#     BaseSkin.trace_flick_note_tick,
#     BaseSkin.trace_note_red_tick,
#     BaseSkin.trace_note_red_tick_fallback,
# )
# critical_trace_tick_sprite_candidates = (
#     BaseSkin.critical_trace_note_tick,
#     BaseSkin.trace_note_yellow_tick,
#     BaseSkin.trace_note_yellow_tick_fallback,
# )
# critical_trace_flick_tick_sprite_candidates = (
#     BaseSkin.critical_trace_flick_note_tick,
#     BaseSkin.critical_trace_note_tick,
#     BaseSkin.trace_note_yellow_tick,
#     BaseSkin.trace_note_yellow_tick_fallback,
# )
#
# normal_active_slide_connector_sprite_candidates = (
#     normal_active_slide_connector_sprites,
#     active_slide_connector_green_sprites,
#     active_slide_connector_green_fallback_sprites,
# )
# critical_active_slide_connector_sprite_candidates = (
#     critical_active_slide_connector_sprites,
#     active_slide_connector_yellow_sprites,
#     active_slide_connector_yellow_fallback_sprites,
# )


@level_data
class ActiveSkin:
    cover: Sprite

    lane: Sprite
    judgment_line: Sprite
    stage_left_border: Sprite
    stage_right_border: Sprite

    sekai_stage: Sprite

    sim_line: Sprite

    normal_note: NoteSpriteSet
    slide_note: NoteSpriteSet
    flick_note: NoteSpriteSet
    down_flick_note: NoteSpriteSet
    critical_note: NoteSpriteSet
    critical_slide_note: NoteSpriteSet
    critical_flick_note: NoteSpriteSet
    critical_down_flick_note: NoteSpriteSet
    trace_note: NoteSpriteSet
    trace_flick_note: NoteSpriteSet
    trace_down_flick_note: NoteSpriteSet
    critical_trace_note: NoteSpriteSet
    critical_trace_flick_note: NoteSpriteSet
    critical_trace_down_flick_note: NoteSpriteSet
    normal_slide_tick_note: NoteSpriteSet
    critical_slide_tick_note: NoteSpriteSet
    damage_note: NoteSpriteSet

    active_slide_connector: ActiveConnectorSpriteSet
    critical_active_slide_connector: ActiveConnectorSpriteSet

    guide_green: Sprite
    guide_yellow: Sprite
    guide_red: Sprite
    guide_purple: Sprite
    guide_cyan: Sprite
    guide_blue: Sprite
    guide_neutral: Sprite
    guide_black: Sprite

    beat_line: Sprite
    bpm_change_line: Sprite
    timescale_change_line: Sprite
    special_line: Sprite


def init_skin():
    ActiveSkin.cover = BaseSkin.cover

    ActiveSkin.lane = BaseSkin.lane
    ActiveSkin.judgment_line = BaseSkin.judgment_line
    ActiveSkin.stage_left_border = BaseSkin.stage_left_border
    ActiveSkin.stage_right_border = BaseSkin.stage_right_border

    ActiveSkin.sekai_stage = BaseSkin.sekai_stage

    ActiveSkin.sim_line = BaseSkin.sim_line

    ActiveSkin.normal_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            normal_note_body_sprites,
            note_cyan_body_sprites,
            note_cyan_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_normal,
            BaseSkin.slot_cyan,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_normal,
            BaseSkin.slot_glow_cyan,
        ),
    )
    ActiveSkin.slide_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            slide_note_body_sprites,
            note_green_body_sprites,
            note_green_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_slide,
            BaseSkin.slot_green,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_slide,
            BaseSkin.slot_glow_green,
        ),
    )
    ActiveSkin.flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            flick_note_body_sprites,
            note_red_body_sprites,
            note_red_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            flick_arrow_sprites,
            flick_arrow_red_sprites,
            flick_arrow_red_fallback_sprites,
        ),
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_flick,
            BaseSkin.slot_red,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_flick,
            BaseSkin.slot_glow_red,
        ),
    )
    ActiveSkin.down_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            down_flick_note_body_sprites,
            flick_note_body_sprites,
            note_red_body_sprites,
            note_red_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            flick_arrow_sprites,
            flick_arrow_red_sprites,
            flick_arrow_red_fallback_sprites,
        ),
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_down_flick,
            BaseSkin.slot_flick,
            BaseSkin.slot_red,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_down_flick,
            BaseSkin.slot_glow_flick,
            BaseSkin.slot_glow_red,
        ),
    )
    ActiveSkin.critical_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_note_body_sprites,
            note_yellow_body_sprites,
            note_yellow_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_critical,
            BaseSkin.slot_yellow,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_critical,
            BaseSkin.slot_glow_yellow,
        ),
    )
    ActiveSkin.critical_slide_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_slide_note_body_sprites,
            critical_note_body_sprites,
            note_yellow_body_sprites,
            note_yellow_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_critical_slide,
            BaseSkin.slot_yellow_slider,
            BaseSkin.slot_critical,
            BaseSkin.slot_yellow,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_critical_slide,
            BaseSkin.slot_glow_yellow_slider_tap,
            BaseSkin.slot_glow_critical,
            BaseSkin.slot_glow_yellow,
        ),
    )
    ActiveSkin.critical_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_flick_note_body_sprites,
            critical_note_body_sprites,
            note_yellow_body_sprites,
            note_yellow_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            critical_flick_arrow_sprites,
            flick_arrow_yellow_sprites,
            flick_arrow_yellow_fallback_sprites,
        ),
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_critical_flick,
            BaseSkin.slot_yellow_flick,
            BaseSkin.slot_critical,
            BaseSkin.slot_yellow,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_critical_flick,
            BaseSkin.slot_glow_yellow_flick,
            BaseSkin.slot_glow_critical,
            BaseSkin.slot_glow_yellow,
        ),
    )
    ActiveSkin.critical_down_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_down_flick_note_body_sprites,
            critical_flick_note_body_sprites,
            critical_note_body_sprites,
            note_yellow_body_sprites,
            note_yellow_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            critical_flick_arrow_sprites,
            flick_arrow_yellow_sprites,
            flick_arrow_yellow_fallback_sprites,
        ),
        tick=EMPTY_SPRITE,
        slot=first_available_sprite(
            BaseSkin.slot_critical_down_flick,
            BaseSkin.slot_critical_flick,
            BaseSkin.slot_yellow_flick,
            BaseSkin.slot_critical,
            BaseSkin.slot_yellow,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.slot_glow_critical_down_flick,
            BaseSkin.slot_glow_critical_flick,
            BaseSkin.slot_glow_yellow_flick,
            BaseSkin.slot_glow_critical,
            BaseSkin.slot_glow_yellow,
        ),
    )
    ActiveSkin.trace_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            normal_trace_note_body_sprites,
            trace_note_green_body_sprites,
            trace_note_green_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.normal_trace_note_tick,
            BaseSkin.trace_note_green_tick,
            BaseSkin.trace_note_green_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.trace_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            trace_flick_note_body_sprites,
            trace_note_red_body_sprites,
            trace_note_red_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            flick_arrow_sprites,
            flick_arrow_red_sprites,
            flick_arrow_red_fallback_sprites,
        ),
        tick=first_available_sprite(
            BaseSkin.trace_flick_note_tick,
            BaseSkin.trace_note_red_tick,
            BaseSkin.trace_note_red_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.trace_down_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            trace_down_flick_note_body_sprites,
            trace_flick_note_body_sprites,
            trace_note_red_body_sprites,
            trace_note_red_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            flick_arrow_sprites,
            flick_arrow_red_sprites,
            flick_arrow_red_fallback_sprites,
        ),
        tick=first_available_sprite(
            BaseSkin.trace_down_flick_note_tick,
            BaseSkin.trace_flick_note_tick,
            BaseSkin.trace_note_red_tick,
            BaseSkin.trace_note_red_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.critical_trace_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_trace_note_body_sprites,
            trace_note_yellow_body_sprites,
            trace_note_yellow_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.critical_trace_note_tick,
            BaseSkin.trace_note_yellow_tick,
            BaseSkin.trace_note_yellow_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.critical_trace_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_trace_flick_note_body_sprites,
            critical_trace_note_body_sprites,
            trace_note_yellow_body_sprites,
            trace_note_yellow_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            critical_flick_arrow_sprites,
            flick_arrow_yellow_sprites,
            flick_arrow_yellow_fallback_sprites,
        ),
        tick=first_available_sprite(
            BaseSkin.critical_trace_flick_note_tick,
            BaseSkin.critical_trace_note_tick,
            BaseSkin.trace_note_yellow_tick,
            BaseSkin.trace_note_yellow_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.critical_trace_down_flick_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            critical_trace_down_flick_note_body_sprites,
            critical_trace_flick_note_body_sprites,
            critical_trace_note_body_sprites,
            trace_note_yellow_body_sprites,
            trace_note_yellow_fallback_body_sprites,
        ),
        arrow=first_available_arrow_sprite_set(
            critical_flick_arrow_sprites,
            flick_arrow_yellow_sprites,
            flick_arrow_yellow_fallback_sprites,
        ),
        tick=first_available_sprite(
            BaseSkin.critical_trace_down_flick_note_tick,
            BaseSkin.critical_trace_flick_note_tick,
            BaseSkin.critical_trace_note_tick,
            BaseSkin.trace_note_yellow_tick,
            BaseSkin.trace_note_yellow_tick_fallback,
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.normal_slide_tick_note = NoteSpriteSet(
        body=EMPTY_BODY_SPRITE_SET,
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.normal_slide_tick_note, BaseSkin.slide_tick_note_green, BaseSkin.slide_tick_note_green_fallback
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.critical_slide_tick_note = NoteSpriteSet(
        body=EMPTY_BODY_SPRITE_SET,
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.critical_slide_tick_note, BaseSkin.slide_tick_note_yellow, BaseSkin.slide_tick_note_yellow_fallback
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )
    ActiveSkin.damage_note = NoteSpriteSet(
        body=first_available_body_sprite_set(
            damage_note_body_sprites,
            trace_note_purple_body_sprites,
            trace_note_purple_fallback_body_sprites,
        ),
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=EMPTY_SPRITE,
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SPRITE,
    )

    ActiveSkin.active_slide_connector = ActiveConnectorSpriteSet(
        connection=first_available_active_connection_sprite_set(
            normal_active_slide_connector_sprites,
            active_slide_connector_green_sprites,
            active_slide_connector_green_fallback_sprites,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.normal_slide_connector_slot_glow,
            BaseSkin.slot_glow_slide,
            BaseSkin.slot_glow_green,
        ),
    )
    ActiveSkin.critical_active_slide_connector = ActiveConnectorSpriteSet(
        connection=first_available_active_connection_sprite_set(
            critical_active_slide_connector_sprites,
            active_slide_connector_yellow_sprites,
            active_slide_connector_yellow_fallback_sprites,
        ),
        slot_glow=first_available_sprite(
            BaseSkin.critical_slide_connector_slot_glow,
            BaseSkin.slot_glow_critical_slide,
            BaseSkin.slot_glow_yellow_slider_tap,
            BaseSkin.slot_glow_critical,
            BaseSkin.slot_glow_yellow,
        ),
    )

    ActiveSkin.guide_green = first_available_sprite(
        BaseSkin.guide_green,
        BaseSkin.guide_green_fallback,
    )
    ActiveSkin.guide_yellow = first_available_sprite(
        BaseSkin.guide_yellow,
        BaseSkin.guide_yellow_fallback,
    )
    ActiveSkin.guide_red = first_available_sprite(
        BaseSkin.guide_red,
        BaseSkin.guide_red_fallback,
    )
    ActiveSkin.guide_purple = first_available_sprite(
        BaseSkin.guide_purple,
        BaseSkin.guide_purple_fallback,
    )
    ActiveSkin.guide_cyan = first_available_sprite(
        BaseSkin.guide_cyan,
        BaseSkin.guide_cyan_fallback,
    )
    ActiveSkin.guide_blue = first_available_sprite(
        BaseSkin.guide_blue,
        BaseSkin.guide_blue_fallback,
    )
    ActiveSkin.guide_neutral = first_available_sprite(
        BaseSkin.guide_neutral,
        BaseSkin.guide_neutral_fallback,
    )
    ActiveSkin.guide_black = first_available_sprite(
        BaseSkin.guide_black,
        BaseSkin.guide_black_fallback,
    )

    ActiveSkin.beat_line = BaseSkin.beat_line
    ActiveSkin.bpm_change_line = BaseSkin.bpm_change_line
    ActiveSkin.timescale_change_line = BaseSkin.timescale_change_line
    ActiveSkin.special_line = BaseSkin.special_line
