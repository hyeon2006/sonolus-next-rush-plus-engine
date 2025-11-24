from __future__ import annotations

from sonolus.script.bucket import Judgment
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

    normal_slot_glow: Sprite = sprite("Sekai Slot Glow Cyan")
    normal_slot_glow_great: Sprite = sprite("Sekai Slot Glow Cyan Great")
    normal_slot_glow_good: Sprite = sprite("Sekai Slot Glow Cyan Good")
    slide_slot_glow: Sprite = sprite("Sekai Slot Glow Green")
    flick_slot_glow: Sprite = sprite("Sekai Slot Glow Red")
    critical_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow")
    critical_flick_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow Flick")
    critical_slide_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow Slider Tap")

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

    damage_note_left: Sprite = sprite("Sekai Trace Note Purple Left")
    damage_note_middle: Sprite = sprite("Sekai Trace Note Purple Middle")
    damage_note_right: Sprite = sprite("Sekai Trace Note Purple Right")
    damage_note_fallback: StandardSprite.NOTE_HEAD_PURPLE
    damage_tick_note: Sprite = sprite("Sekai Trace Diamond Purple")
    damage_tick_note_fallback: StandardSprite.NOTE_TICK_RED

    beat_line: StandardSprite.GRID_NEUTRAL
    bpm_change_line: StandardSprite.GRID_PURPLE
    timescale_change_line: StandardSprite.GRID_YELLOW
    special_line: StandardSprite.GRID_RED

    # Custom Elements
    perfect: Sprite = sprite("Perfect")
    great: Sprite = sprite("Great")
    good: Sprite = sprite("Good")
    bad: Sprite = sprite("Bad")
    miss: Sprite = sprite("Miss")
    auto: Sprite = sprite("Auto")
    ap_number: SpriteGroup = sprite_group(f"AP Combo Number {i}" for i in range(10))
    combo_number: SpriteGroup = sprite_group(f"Combo Number {i}" for i in range(10))
    combo_number_glow: SpriteGroup = sprite_group(f"Combo Number Glow {i}" for i in range(10))
    ap_combo_label: Sprite = sprite("AP Combo Label")
    combo_label: Sprite = sprite("Combo Label")
    combo_label_glow: Sprite = sprite("Combo Label Glow")
    fast_warning: Sprite = sprite("Fast Warning")
    late_warning: Sprite = sprite("Late Warning")
    flick_warning: Sprite = sprite("Flick Warning")
    damage_flash: Sprite = sprite("Damage Flash")
    auto_live: Sprite = sprite("Auto Live")


class BodySprites(Record):
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


class ComboNumberSprite(Record):
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
    def custom_available(self):
        return self.normal[0].is_available


class ComboLabelSprite(Record):
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
    def custom_available(self):
        return self.normal.is_available


class JudgmentSprite(Record):
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
    def custom_available(self):
        return self.perfect.is_available


class AccuracySprite(Record):
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
    def custom_available(self):
        return self.fast.is_available


class DamageFlashSprite(Record):
    normal: Sprite

    def get_sprite(self):
        return self.normal

    @property
    def custom_available(self):
        return self.normal.is_available


normal_note_body_sprites = BodySprites(
    left=Skin.normal_note_left,
    middle=Skin.normal_note_middle,
    right=Skin.normal_note_right,
    fallback=Skin.normal_note_fallback,
)
slide_note_body_sprites = BodySprites(
    left=Skin.slide_note_left,
    middle=Skin.slide_note_middle,
    right=Skin.slide_note_right,
    fallback=Skin.slide_note_fallback,
)
flick_note_body_sprites = BodySprites(
    left=Skin.flick_note_left,
    middle=Skin.flick_note_middle,
    right=Skin.flick_note_right,
    fallback=Skin.flick_note_fallback,
)
critical_note_body_sprites = BodySprites(
    left=Skin.critical_note_left,
    middle=Skin.critical_note_middle,
    right=Skin.critical_note_right,
    fallback=Skin.critical_note_fallback,
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
damage_tick_sprites = TickSprites(
    normal=Skin.damage_tick_note,
    fallback=Skin.trace_flick_tick_note_fallback,
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

neutral_guide_sprites = GuideSprites(
    normal=Skin.guide_neutral,
    fallback=Skin.guide_neutral_fallback,
)
red_guide_sprites = GuideSprites(
    normal=Skin.guide_red,
    fallback=Skin.guide_red_fallback,
)
green_guide_sprites = GuideSprites(
    normal=Skin.guide_green,
    fallback=Skin.guide_green_fallback,
)
blue_guide_sprites = GuideSprites(
    normal=Skin.guide_blue,
    fallback=Skin.guide_blue_fallback,
)
yellow_guide_sprites = GuideSprites(
    normal=Skin.guide_yellow,
    fallback=Skin.guide_yellow_fallback,
)
purple_guide_sprites = GuideSprites(
    normal=Skin.guide_purple,
    fallback=Skin.guide_purple_fallback,
)
cyan_guide_sprites = GuideSprites(
    normal=Skin.guide_cyan,
    fallback=Skin.guide_cyan_fallback,
)
black_guide_sprites = GuideSprites(
    normal=Skin.guide_black,
    fallback=Skin.guide_black_fallback,
)
combo_number = ComboNumberSprite(
    normal=Skin.combo_number,
    ap=Skin.ap_number,
    glow=Skin.combo_number_glow,
)
combo_label = ComboLabelSprite(normal=Skin.combo_label, ap=Skin.ap_combo_label, glow=Skin.combo_label_glow)
judgment_text = JudgmentSprite(
    perfect=Skin.perfect, great=Skin.great, good=Skin.good, bad=Skin.bad, miss=Skin.miss, auto=Skin.auto
)
accuracy_text = AccuracySprite(
    fast=Skin.fast_warning,
    late=Skin.late_warning,
    flick=Skin.flick_warning,
)
damage_flash = DamageFlashSprite(normal=Skin.damage_flash)
