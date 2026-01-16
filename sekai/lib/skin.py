from __future__ import annotations

from enum import IntEnum
from typing import Self, assert_never

from sonolus.script.bucket import Judgment
from sonolus.script.globals import level_data
from sonolus.script.interval import Interval, clamp
from sonolus.script.record import Record
from sonolus.script.runtime import is_replay, is_watch
from sonolus.script.sprite import Sprite, SpriteGroup, StandardSprite, skin, sprite, sprite_group

from sekai.lib.layout import AccuracyType, ComboType, FlickDirection, JudgmentType
from sekai.lib.options import Options


@skin
class BaseSkin:
    cover: StandardSprite.STAGE_COVER
    background: Sprite = sprite("Sekai Black Background")

    lane: StandardSprite.LANE
    judgment_line: StandardSprite.JUDGMENT_LINE
    stage_left_border: StandardSprite.STAGE_LEFT_BORDER
    stage_right_border: StandardSprite.STAGE_RIGHT_BORDER

    sekai_stage: Sprite = sprite("Sekai Stage")
    sekai_stage_lane: Sprite = sprite("Sekai Stage Lane")
    sekai_stage_cover: Sprite = sprite("Sekai Stage Cover")

    sekai_stage_fever: Sprite = sprite("Sekai Stage Fever")
    sekai_stage_fever_tablet: Sprite = sprite("Sekai Stage Fever Tablet")
    sekai_fever_gauge_yellow: Sprite = sprite("Sekai Fever Gauge Yellow")
    sekai_fever_gauge_rainbow: Sprite = sprite("Sekai Fever Gauge Rainbow")

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
    slot_glow_cyan_great: Sprite = sprite("Sekai Slot Glow Cyan Great")
    slot_glow_cyan_good: Sprite = sprite("Sekai Slot Glow Cyan Good")
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
    skill_line: StandardSprite.GRID_GREEN
    fever_chance_line: StandardSprite.GRID_CYAN
    fever_start_line: StandardSprite.GRID_BLUE

    # Custom Elements
    perfect: Sprite = sprite("Perfect")
    great: Sprite = sprite("Great")
    good: Sprite = sprite("Good")
    bad: Sprite = sprite("Bad")
    miss: Sprite = sprite("Miss")
    auto: Sprite = sprite("Auto")
    ap_combo_number: SpriteGroup = sprite_group(f"AP Combo Number {i}" for i in range(12))
    combo_number: SpriteGroup = sprite_group(f"Combo Number {i}" for i in range(12))
    combo_number_glow: SpriteGroup = sprite_group(f"Combo Number Glow {i}" for i in range(12))
    ap_combo_label: Sprite = sprite("AP Combo Label")
    combo_label: Sprite = sprite("Combo Label")
    combo_label_glow: Sprite = sprite("Combo Label Glow")
    fast_warning: Sprite = sprite("Fast Warning")
    late_warning: Sprite = sprite("Late Warning")
    flick_warning: Sprite = sprite("Flick Warning")
    damage_flash: Sprite = sprite("Damage Flash")
    auto_live: Sprite = sprite("Auto Live")
    skill_bar: Sprite = sprite("Skill Bar")
    skill_level: Sprite = sprite("Skill Level")
    skill_percent: Sprite = sprite("Skill Percent")
    skill_value: Sprite = sprite("Skill Value")
    skill_icon: SpriteGroup = sprite_group(f"Skill Icon {i}" for i in range(1, 6))
    ui_number: SpriteGroup = sprite_group(f"UI Number {i}" for i in range(12))
    life_bar_pause: Sprite = sprite("Life Bar Pause")
    life_bar_skip: Sprite = sprite("Life Bar Skip")
    life_bar_disable: Sprite = sprite("Life Bar Disable")
    life_bar_gauge_normal: Sprite = sprite("Life Bar Gauge Normal")
    life_bar_gauge_danger: Sprite = sprite("Life Bar Gauge Danger")
    score_bar: Sprite = sprite("Score Bar")
    score_bar_panel: Sprite = sprite("Score Bar Panel")
    score_bar_gauge: Sprite = sprite("Score Bar Gauge")
    score_bar_mask: Sprite = sprite("Score Bar Mask")
    score_rank_s: Sprite = sprite("Score Rank S")
    score_rank_a: Sprite = sprite("Score Rank A")
    score_rank_b: Sprite = sprite("Score Rank B")
    score_rank_c: Sprite = sprite("Score Rank C")
    score_rank_d: Sprite = sprite("Score Rank D")
    score_rank_text_s: Sprite = sprite("Score Rank Text S")
    score_rank_text_a: Sprite = sprite("Score Rank Text A")
    score_rank_text_b: Sprite = sprite("Score Rank Text B")
    score_rank_text_c: Sprite = sprite("Score Rank Text C")
    score_rank_text_d: Sprite = sprite("Score Rank Text D")


EMPTY_SPRITE = Sprite(-1)
EMPTY_SPRITE_GROUP = SpriteGroup(-1, 1)

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


class SlotGlowSpriteSet(Record):
    perfect: Sprite
    great: Sprite
    good: Sprite

    def get_sprite(self, judgment: Judgment = Judgment.PERFECT):
        result = +Sprite
        match judgment:
            case Judgment.PERFECT:
                result @= self.perfect
            case Judgment.GREAT:
                result @= self.great
            case _:
                result @= self.good
        return result

    @property
    def available(self):
        return self.perfect.is_available


EMPTY_SLOT_GLOW_SPRITE_SET = SlotGlowSpriteSet(
    perfect=EMPTY_SPRITE,
    great=EMPTY_SPRITE,
    good=EMPTY_SPRITE,
)


def first_available_slot_glow_sprite_set(*sets: SlotGlowSpriteSet) -> SlotGlowSpriteSet:
    result = +EMPTY_SLOT_GLOW_SPRITE_SET
    for s in sets:
        if s.available:
            result @= s
            break
    return result


class ComboNumberSpriteSet(Record):
    normal: SpriteGroup
    ap: SpriteGroup
    glow: SpriteGroup

    def get_sprite(self, combo: int, combo_type: ComboType):
        result = +Sprite
        match combo_type:
            case ComboType.NORMAL:
                result @= self.normal[combo]
            case ComboType.AP:
                result @= self.ap[combo]
            case ComboType.GLOW:
                result @= self.glow[combo]
            case _:
                assert_never(combo_type)
        return result

    @property
    def available(self):
        return self.normal[0].is_available


class ComboLabelSpriteSet(Record):
    normal: Sprite
    ap: Sprite
    glow: Sprite

    def get_sprite(self, combo_type: ComboType):
        result = +Sprite
        match combo_type:
            case ComboType.NORMAL:
                result @= self.normal
            case ComboType.AP:
                result @= self.ap
            case ComboType.GLOW:
                result @= self.glow
            case _:
                assert_never(combo_type)
        return result

    @property
    def available(self):
        return self.normal.is_available


class JudgmentSpriteSet(Record):
    perfect: Sprite
    great: Sprite
    good: Sprite
    bad: Sprite
    miss: Sprite
    auto: Sprite

    def get_bad(self, judgment: Judgment, windows_bad: Interval, accuracy: float, check_pass: bool):
        if Options.auto_judgment and is_watch() and not is_replay():
            return JudgmentType.AUTO
        elif (
            judgment == Judgment.MISS
            and windows_bad != Interval(-1, -1)
            and (windows_bad.start <= accuracy <= windows_bad.end or windows_bad == Interval(0, 0))
            and check_pass
        ):
            return JudgmentType.BAD
        else:
            return judgment

    def get_sprite(self, judgment_type: Judgment, windows_bad: Interval, accuracy: float, check_pass: bool):
        result = +Sprite
        match self.get_bad(judgment_type, windows_bad, accuracy, check_pass):
            case JudgmentType.PERFECT:
                result @= self.perfect
            case JudgmentType.GREAT:
                result @= self.great
            case JudgmentType.GOOD:
                result @= self.good
            case JudgmentType.BAD:
                result @= self.bad
            case JudgmentType.MISS:
                result @= self.miss
            case JudgmentType.AUTO:
                result @= self.auto
        return result

    @property
    def available(self):
        return self.perfect.is_available


class AccuracySpriteSet(Record):
    fast: Sprite
    late: Sprite
    flick: Sprite

    def get_accuracy(self, judgment: Judgment, windows: Interval, accuracy: float, wrong_way: bool) -> AccuracyType:
        if judgment != Judgment.PERFECT:
            if wrong_way:
                return AccuracyType.Flick
            elif windows.start > accuracy:
                return AccuracyType.Fast
            else:
                return AccuracyType.Late
        else:
            return AccuracyType.NONE

    def get_sprite(self, judgment: Judgment, windows: Interval, accuracy: float, wrong_way: bool):
        result = +Sprite
        match self.get_accuracy(judgment, windows, accuracy, wrong_way):
            case AccuracyType.Fast:
                result @= self.fast
            case AccuracyType.Late:
                result @= self.late
            case AccuracyType.Flick:
                result @= self.flick
        return result

    @property
    def available(self):
        return self.fast.is_available


class FeverGaugeSpriteSet(Record):
    yellow: Sprite
    rainbow: Sprite

    def get_sprite(self, percentage: float):
        result = +Sprite
        if percentage >= 0.78:
            result @= self.rainbow
        else:
            result @= self.yellow
        return result

    @property
    def available(self):
        return self.yellow.is_available


class SkillIconSpriteSet(Record):
    icon: SpriteGroup

    def get_sprite(self, num: int):
        result = +Sprite
        result = self.icon[(num) % 5]
        return result

    @property
    def available(self):
        return self.icon[0].is_available


class UINumberSpriteSet(Record):
    ui: SpriteGroup

    def get_sprite(self, number: int):
        return self.ui[number]

    @property
    def available(self):
        return self.ui[0].is_available


class LifeBarType(IntEnum):
    PAUSE = 0
    SKIP = 1
    DISABLE = 2


class LifeBarSpriteSet(Record):
    pause: Sprite
    skip: Sprite
    disable: Sprite

    def get_sprite(self, bar_type: LifeBarType):
        result = +Sprite
        match bar_type:
            case LifeBarType.PAUSE:
                result = self.pause
            case LifeBarType.SKIP:
                result = self.skip
            case LifeBarType.DISABLE:
                result = self.disable
            case _:
                assert_never(bar_type)
        return result

    @property
    def available(self):
        return self.pause.is_available


class LifeGaugeSpriteSet(Record):
    normal: Sprite
    danger: Sprite

    def get_sprite(self, life: int):
        result = +Sprite
        if life > 400:
            result @= self.normal
        else:
            result @= self.danger
        return result

    @property
    def available(self):
        return self.normal.is_available


class LifeSpriteSet(Record):
    bar: LifeBarSpriteSet
    gauge: LifeGaugeSpriteSet


class ScoreGaugeType(IntEnum):
    NORMAL = 0
    MASK = 1


class ScoreGaugeSpriteSet(Record):
    normal: Sprite
    mask: Sprite

    def get_sprite(self, gauge_type: ScoreGaugeType):
        result = +Sprite
        match gauge_type:
            case ScoreGaugeType.NORMAL:
                result = self.normal
            case ScoreGaugeType.MASK:
                result = self.mask
            case _:
                assert_never(gauge_type)
        return result

    @property
    def available(self):
        return self.normal.is_available


class ScoreRankType(IntEnum):
    S = 0
    A = 1
    B = 2
    C = 3
    D = 4


class ScoreRankSpriteSet(Record):
    s: Sprite
    a: Sprite
    b: Sprite
    c: Sprite
    d: Sprite

    def get_sprite(self, score_type: ScoreRankType):
        result = +Sprite
        match score_type:
            case ScoreRankType.S:
                result = self.s
            case ScoreRankType.A:
                result = self.a
            case ScoreRankType.B:
                result = self.b
            case ScoreRankType.C:
                result = self.c
            case ScoreRankType.D:
                result = self.d
            case _:
                assert_never(score_type)
        return result

    @property
    def available(self):
        return self.s.is_available


class ScoreSpriteSet(Record):
    bar: Sprite
    panel: Sprite
    gauge: ScoreGaugeSpriteSet
    rank: ScoreRankSpriteSet
    rank_text: ScoreRankSpriteSet


class NoteSpriteSet(Record):
    body: BodySpriteSet
    arrow: ArrowSpriteSet
    tick: Sprite
    slot: Sprite
    slot_glow: SlotGlowSpriteSet


EMPTY_NOTE_SPRITE_SET = NoteSpriteSet(
    body=EMPTY_BODY_SPRITE_SET,
    arrow=EMPTY_ARROW_SPRITE_SET,
    tick=EMPTY_SPRITE,
    slot=EMPTY_SPRITE,
    slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
damage_tick_sprites = TickSprites(
    normal=Skin.damage_tick_note,
    fallback=Skin.trace_flick_tick_note_fallback,
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
slot_glow_cyan_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_cyan, great=BaseSkin.slot_glow_cyan_great, good=BaseSkin.slot_glow_cyan_good
)
slot_glow_green_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_green, great=BaseSkin.slot_glow_green, good=BaseSkin.slot_glow_green
)
slot_glow_red_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_red, great=BaseSkin.slot_glow_red, good=BaseSkin.slot_glow_red
)
slot_glow_yellow_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_yellow, great=BaseSkin.slot_glow_yellow, good=BaseSkin.slot_glow_yellow
)
slot_glow_yellow_flick_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_yellow_flick, great=BaseSkin.slot_glow_yellow_flick, good=BaseSkin.slot_glow_yellow_flick
)
slot_glow_yellow_slider_tap_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_yellow_slider_tap,
    great=BaseSkin.slot_glow_yellow_slider_tap,
    good=BaseSkin.slot_glow_yellow_slider_tap,
)
slot_glow_normal_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_normal, great=BaseSkin.slot_glow_normal, good=BaseSkin.slot_glow_normal
)
slot_glow_slide_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_slide, great=BaseSkin.slot_glow_slide, good=BaseSkin.slot_glow_slide
)
slot_glow_flick_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_flick, great=BaseSkin.slot_glow_flick, good=BaseSkin.slot_glow_flick
)
slot_glow_down_flick_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_down_flick, great=BaseSkin.slot_glow_down_flick, good=BaseSkin.slot_glow_down_flick
)
slot_glow_critical_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_critical, great=BaseSkin.slot_glow_critical, good=BaseSkin.slot_glow_critical
)
slot_glow_critical_slide_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_critical_slide,
    great=BaseSkin.slot_glow_critical_slide,
    good=BaseSkin.slot_glow_critical_slide,
)
slot_glow_critical_flick_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_critical_flick,
    great=BaseSkin.slot_glow_critical_flick,
    good=BaseSkin.slot_glow_critical_flick,
)
slot_glow_critical_down_flick_sprites = SlotGlowSpriteSet(
    perfect=BaseSkin.slot_glow_critical_down_flick,
    great=BaseSkin.slot_glow_critical_down_flick,
    good=BaseSkin.slot_glow_critical_down_flick,
)
life_bar = LifeBarSpriteSet(
    pause=BaseSkin.life_bar_pause, skip=BaseSkin.life_bar_skip, disable=BaseSkin.life_bar_disable
)
life_gauge = LifeGaugeSpriteSet(normal=BaseSkin.life_bar_gauge_normal, danger=BaseSkin.life_bar_gauge_danger)
score_gauge = ScoreGaugeSpriteSet(normal=BaseSkin.score_bar_gauge, mask=BaseSkin.score_bar_mask)
score_rank = ScoreRankSpriteSet(
    s=BaseSkin.score_rank_s,
    a=BaseSkin.score_rank_a,
    b=BaseSkin.score_rank_b,
    c=BaseSkin.score_rank_c,
    d=BaseSkin.score_rank_d,
)
score_rank_text = ScoreRankSpriteSet(
    s=BaseSkin.score_rank_text_s,
    a=BaseSkin.score_rank_text_a,
    b=BaseSkin.score_rank_text_b,
    c=BaseSkin.score_rank_text_c,
    d=BaseSkin.score_rank_text_d,
)


@level_data
class ActiveSkin:
    cover: Sprite
    background: Sprite

    lane: Sprite
    judgment_line: Sprite
    stage_left_border: Sprite
    stage_right_border: Sprite

    sekai_stage: Sprite
    sekai_stage_lane: Sprite
    sekai_stage_cover: Sprite

    sekai_stage_fever: Sprite
    sekai_stage_fever_tablet: Sprite
    sekai_fever_gauge: FeverGaugeSpriteSet

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
    skill_line: Sprite
    fever_chance_line: Sprite
    fever_start_line: Sprite

    judgment: JudgmentSpriteSet
    combo_number: ComboNumberSpriteSet
    combo_label: ComboLabelSpriteSet
    accuracy_warning: AccuracySpriteSet
    damage_flash: Sprite
    auto_live: Sprite
    skill_bar: Sprite
    skill_level: Sprite
    skill_percent: Sprite
    skill_value: Sprite
    skill_icon: SkillIconSpriteSet
    ui_number: UINumberSpriteSet
    life: LifeSpriteSet
    score: ScoreSpriteSet


def init_skin():
    ActiveSkin.cover = BaseSkin.cover
    ActiveSkin.background = BaseSkin.background

    ActiveSkin.lane = BaseSkin.lane
    ActiveSkin.judgment_line = BaseSkin.judgment_line
    ActiveSkin.stage_left_border = BaseSkin.stage_left_border
    ActiveSkin.stage_right_border = BaseSkin.stage_right_border

    ActiveSkin.sekai_stage = BaseSkin.sekai_stage
    ActiveSkin.sekai_stage_lane = BaseSkin.sekai_stage_lane
    ActiveSkin.sekai_stage_cover = BaseSkin.sekai_stage_cover

    ActiveSkin.sekai_stage_fever = BaseSkin.sekai_stage_fever
    ActiveSkin.sekai_stage_fever_tablet = BaseSkin.sekai_stage_fever_tablet
    ActiveSkin.sekai_fever_gauge = FeverGaugeSpriteSet(
        yellow=BaseSkin.sekai_fever_gauge_yellow, rainbow=BaseSkin.sekai_fever_gauge_rainbow
    )

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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_normal_sprites,
            slot_glow_cyan_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_slide_sprites,
            slot_glow_green_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_flick_sprites,
            slot_glow_red_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_down_flick_sprites,
            slot_glow_flick_sprites,
            slot_glow_red_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_critical_sprites,
            slot_glow_yellow_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_critical_slide_sprites,
            slot_glow_yellow_slider_tap_sprites,
            slot_glow_critical_sprites,
            slot_glow_yellow_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_critical_flick_sprites,
            slot_glow_yellow_flick_sprites,
            slot_glow_critical_sprites,
            slot_glow_yellow_sprites,
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
        slot_glow=first_available_slot_glow_sprite_set(
            slot_glow_critical_down_flick_sprites,
            slot_glow_critical_flick_sprites,
            slot_glow_yellow_flick_sprites,
            slot_glow_critical_sprites,
            slot_glow_yellow_sprites,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
    )
    ActiveSkin.normal_slide_tick_note = NoteSpriteSet(
        body=EMPTY_BODY_SPRITE_SET,
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.normal_slide_tick_note, BaseSkin.slide_tick_note_green, BaseSkin.slide_tick_note_green_fallback
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
    )
    ActiveSkin.critical_slide_tick_note = NoteSpriteSet(
        body=EMPTY_BODY_SPRITE_SET,
        arrow=EMPTY_ARROW_SPRITE_SET,
        tick=first_available_sprite(
            BaseSkin.critical_slide_tick_note, BaseSkin.slide_tick_note_yellow, BaseSkin.slide_tick_note_yellow_fallback
        ),
        slot=EMPTY_SPRITE,
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
        slot_glow=EMPTY_SLOT_GLOW_SPRITE_SET,
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
    ActiveSkin.skill_line = BaseSkin.skill_line
    ActiveSkin.fever_chance_line = BaseSkin.fever_chance_line
    ActiveSkin.fever_start_line = BaseSkin.fever_start_line
    ActiveSkin.judgment = JudgmentSpriteSet(
        perfect=BaseSkin.perfect,
        great=BaseSkin.great,
        good=BaseSkin.good,
        bad=BaseSkin.bad,
        miss=BaseSkin.miss,
        auto=BaseSkin.auto,
    )

    ActiveSkin.combo_number = ComboNumberSpriteSet(
        normal=BaseSkin.combo_number, ap=BaseSkin.ap_combo_number, glow=BaseSkin.combo_number_glow
    )
    ActiveSkin.combo_label = ComboLabelSpriteSet(
        normal=BaseSkin.combo_label, ap=BaseSkin.ap_combo_label, glow=BaseSkin.combo_label_glow
    )
    ActiveSkin.accuracy_warning = AccuracySpriteSet(
        fast=BaseSkin.fast_warning, late=BaseSkin.late_warning, flick=BaseSkin.flick_warning
    )
    ActiveSkin.damage_flash = BaseSkin.damage_flash
    ActiveSkin.auto_live = BaseSkin.auto_live
    ActiveSkin.skill_bar = BaseSkin.skill_bar
    ActiveSkin.skill_icon = SkillIconSpriteSet(icon=BaseSkin.skill_icon)
    ActiveSkin.skill_level = BaseSkin.skill_level
    ActiveSkin.skill_percent = BaseSkin.skill_percent
    ActiveSkin.skill_value = BaseSkin.skill_value
    ActiveSkin.ui_number = UINumberSpriteSet(ui=BaseSkin.ui_number)
    ActiveSkin.life = LifeSpriteSet(bar=life_bar, gauge=life_gauge)
    ActiveSkin.score = ScoreSpriteSet(
        bar=BaseSkin.score_bar,
        panel=BaseSkin.score_bar_panel,
        gauge=score_gauge,
        rank=score_rank,
        rank_text=score_rank_text,
    )
