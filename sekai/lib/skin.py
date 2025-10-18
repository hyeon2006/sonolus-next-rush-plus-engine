from typing import assert_never

from sonolus.script.interval import clamp
from sonolus.script.record import Record
from sonolus.script.sprite import Sprite, SpriteGroup, StandardSprite, skin, sprite, sprite_group

from sekai.lib.layout import FlickDirection, JudgmentType, AccuracyType, ComboType

from sonolus.script.bucket import Judgment
from sonolus.script.interval import Interval
from sekai.lib.options import Options
from sonolus.script.runtime import is_watch, is_replay
from sonolus.script.debug import debug_log

@skin
class Skin:
    cover: StandardSprite.STAGE_COVER

    lane: StandardSprite.LANE
    judgment_line: StandardSprite.JUDGMENT_LINE
    stage_left_border: StandardSprite.STAGE_LEFT_BORDER
    stage_right_border: StandardSprite.STAGE_RIGHT_BORDER

    sekai_stage: Sprite = sprite("Sekai Stage")

    sim_line: StandardSprite.SIMULTANEOUS_CONNECTION_NEUTRAL

    normal_note_left: Sprite = sprite("Sekai Note Cyan Left")
    normal_note_middle: Sprite = sprite("Sekai Note Cyan Middle")
    normal_note_right: Sprite = sprite("Sekai Note Cyan Right")
    normal_note_fallback: StandardSprite.NOTE_HEAD_CYAN

    slide_note_left: Sprite = sprite("Sekai Note Green Left")
    slide_note_middle: Sprite = sprite("Sekai Note Green Middle")
    slide_note_right: Sprite = sprite("Sekai Note Green Right")
    slide_note_fallback: StandardSprite.NOTE_HEAD_GREEN
    slide_note_end_fallback: StandardSprite.NOTE_TAIL_GREEN

    flick_note_left: Sprite = sprite("Sekai Note Red Left")
    flick_note_middle: Sprite = sprite("Sekai Note Red Middle")
    flick_note_right: Sprite = sprite("Sekai Note Red Right")
    flick_note_fallback: StandardSprite.NOTE_HEAD_RED
    flick_note_end_fallback: StandardSprite.NOTE_TAIL_RED

    critical_note_left: Sprite = sprite("Sekai Note Yellow Left")
    critical_note_middle: Sprite = sprite("Sekai Note Yellow Middle")
    critical_note_right: Sprite = sprite("Sekai Note Yellow Right")
    critical_note_fallback: StandardSprite.NOTE_HEAD_YELLOW
    critical_note_end_fallback: StandardSprite.NOTE_TAIL_YELLOW

    normal_slide_tick_note: Sprite = sprite("Sekai Diamond Green")
    normal_slide_tick_note_fallback: StandardSprite.NOTE_TICK_GREEN

    critical_slide_tick_note: Sprite = sprite("Sekai Diamond Yellow")
    critical_slide_tick_note_fallback: StandardSprite.NOTE_TICK_YELLOW

    normal_slide_connector_normal: Sprite = sprite("Sekai Active Slide Connection Green")
    normal_slide_connector_active: Sprite = sprite("Sekai Active Slide Connection Green Active")
    normal_slide_connector_fallback: StandardSprite.NOTE_CONNECTION_GREEN_SEAMLESS

    critical_slide_connector_normal: Sprite = sprite("Sekai Active Slide Connection Yellow")
    critical_slide_connector_active: Sprite = sprite("Sekai Active Slide Connection Yellow Active")
    critical_slide_connector_fallback: StandardSprite.NOTE_CONNECTION_YELLOW_SEAMLESS

    normal_slot: Sprite = sprite("Sekai Slot Cyan")
    slide_slot: Sprite = sprite("Sekai Slot Green")
    flick_slot: Sprite = sprite("Sekai Slot Red")
    critical_slot: Sprite = sprite("Sekai Slot Yellow")
    critical_flick_slot: Sprite = sprite("Sekai Slot Yellow Flick")
    critical_slide_slot: Sprite = sprite("Sekai Slot Yellow Slider")

    normal_slot_glow: Sprite = sprite("Sekai Slot Glow Cyan")
    slide_slot_glow: Sprite = sprite("Sekai Slot Glow Green")
    flick_slot_glow: Sprite = sprite("Sekai Slot Glow Red")
    critical_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow")
    critical_flick_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow Flick")
    critical_slide_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow Slider Tap")

    normal_slide_connector_slot_glow: Sprite = sprite("Sekai Slot Glow Green Slider Hold")
    critical_slide_connector_slot_glow: Sprite = sprite("Sekai Slot Glow Yellow Slider Hold")

    flick_arrow_up: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Up {i}" for i in range(1, 7))
    flick_arrow_up_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Up Left {i}" for i in range(1, 7))
    flick_arrow_down: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Down {i}" for i in range(1, 7))
    flick_arrow_down_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Red Down Left {i}" for i in range(1, 7))
    flick_arrow_fallback: StandardSprite.DIRECTIONAL_MARKER_RED

    critical_arrow_up: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Up {i}" for i in range(1, 7))
    critical_arrow_up_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Up Left {i}" for i in range(1, 7))
    critical_arrow_down: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Down {i}" for i in range(1, 7))
    critical_arrow_down_left: SpriteGroup = sprite_group(f"Sekai Flick Arrow Yellow Down Left {i}" for i in range(1, 7))
    critical_arrow_fallback: StandardSprite.DIRECTIONAL_MARKER_YELLOW

    normal_trace_note_left: Sprite = sprite("Sekai Trace Note Green Left")
    normal_trace_note_middle: Sprite = sprite("Sekai Trace Note Green Middle")
    normal_trace_note_right: Sprite = sprite("Sekai Trace Note Green Right")
    normal_trace_note_fallback: StandardSprite.NOTE_HEAD_GREEN
    normal_trace_tick_note: Sprite = sprite("Sekai Trace Diamond Green")
    normal_trace_tick_note_fallback: StandardSprite.NOTE_TICK_GREEN

    critical_trace_note_left: Sprite = sprite("Sekai Trace Note Yellow Left")
    critical_trace_note_middle: Sprite = sprite("Sekai Trace Note Yellow Middle")
    critical_trace_note_right: Sprite = sprite("Sekai Trace Note Yellow Right")
    critical_trace_note_fallback: StandardSprite.NOTE_HEAD_YELLOW
    critical_trace_tick_note: Sprite = sprite("Sekai Trace Diamond Yellow")
    critical_trace_tick_note_fallback: StandardSprite.NOTE_TICK_YELLOW

    trace_flick_note_left: Sprite = sprite("Sekai Trace Note Red Left")
    trace_flick_note_middle: Sprite = sprite("Sekai Trace Note Red Middle")
    trace_flick_note_right: Sprite = sprite("Sekai Trace Note Red Right")
    trace_flick_note_fallback: StandardSprite.NOTE_HEAD_RED
    trace_flick_tick_note: Sprite = sprite("Sekai Trace Diamond Red")
    trace_flick_tick_note_fallback: StandardSprite.NOTE_TICK_RED

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
    ap_number: SpriteGroup = sprite_group(f"AP Combo Number {i}" for i in range(0, 10))
    combo_number: SpriteGroup = sprite_group(f"Combo Number {i}" for i in range(0, 10))
    combo_number_glow: SpriteGroup = sprite_group(f"Combo Number Glow {i}" for i in range(0, 10))
    combo_label: Sprite = sprite("Combo Label")
    ap_combo_label: Sprite = sprite("AP Combo Label")
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
    fallback: Sprite

    @property
    def custom_available(self):
        return self.left.is_available


class ArrowSprites(Record):
    up: SpriteGroup
    up_left: SpriteGroup
    down: SpriteGroup
    down_left: SpriteGroup
    fallback: Sprite

    def _get_index_from_size(self, size: float) -> int:
        return int(clamp(round(size * 2), 1, 6)) - 1

    def get_sprite(self, size: float, direction: FlickDirection) -> Sprite:
        result = +Sprite
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
        return result

    @property
    def custom_available(self):
        return self.up_left[0].is_available


class TickSprites(Record):
    normal: Sprite
    fallback: Sprite

    @property
    def custom_available(self):
        return self.normal.is_available


class ActiveConnectorSprites(Record):
    normal: Sprite
    active: Sprite
    fallback: Sprite

    @property
    def custom_available(self):
        return self.normal.is_available


class GuideSprites(Record):
    normal: Sprite
    fallback: Sprite

    @property
    def custom_available(self):
        return self.normal.is_available


class ComboNumberSprite(Record):
    normal: SpriteGroup
    ap: SpriteGroup
    glow: SpriteGroup
    
    def get_sprite(self, combo: int, type: ComboType):
        result = +Sprite
        match type:
            case ComboType.NORMAL:
                result @= self.normal[combo]
            case ComboType.AP:
                result @= self.ap[combo]
            case ComboType.GLOW:
                result @= self.glow[combo]
            case _:
                assert_never(type)
        return result
    
    @property
    def custom_available(self):
        return self.normal[0].is_available


class ComboLabelSprite(Record):
    normal: Sprite
    ap: Sprite
    glow: Sprite
    
    def get_sprite(self, type: ComboType):
        result = +Sprite
        match type:
            case ComboType.NORMAL:
                result @= self.normal
            case ComboType.AP:
                result @= self.ap
            case ComboType.GLOW:
                result @= self.glow
            case _:
                assert_never(type)
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
        elif windows_bad != Interval(0, 0) and windows_bad.start <= accuracy <= windows_bad.end and not check_pass:
            return JudgmentType.BAD
        else:
            return judgment
    
    def get_sprite(self, type: Judgment, windows_bad: Interval, accuracy: float, check_pass: bool):
        result = +Sprite
        match self.get_bad(type, windows_bad, accuracy, check_pass):
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
            case _:
                assert_never(type)
        return result
    
    @property
    def custom_available(self):
        return self.perfect.is_available


class AccuracySprite(Record):
    fast: Sprite
    late: Sprite
    flick: Sprite
    
    def get_accuracy(self, judgment: Judgment, windows: Interval, accuracy: float, wrong_way: bool):
        if judgment != Judgment.PERFECT and judgment != Judgment.MISS:
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
            case _:
                assert_never(type)
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

normal_trace_note_body_sprites = BodySprites(
    left=Skin.normal_trace_note_left,
    middle=Skin.normal_trace_note_middle,
    right=Skin.normal_trace_note_right,
    fallback=Skin.normal_trace_note_fallback,
)
critical_trace_note_body_sprites = BodySprites(
    left=Skin.critical_trace_note_left,
    middle=Skin.critical_trace_note_middle,
    right=Skin.critical_trace_note_right,
    fallback=Skin.critical_trace_note_fallback,
)
trace_flick_note_body_sprites = BodySprites(
    left=Skin.trace_flick_note_left,
    middle=Skin.trace_flick_note_middle,
    right=Skin.trace_flick_note_right,
    fallback=Skin.trace_flick_note_fallback,
)
trace_slide_note_body_sprites = normal_trace_note_body_sprites

damage_note_body_sprites = BodySprites(
    left=Skin.damage_note_left,
    middle=Skin.damage_note_middle,
    right=Skin.damage_note_right,
    fallback=Skin.damage_note_fallback,
)

normal_arrow_sprites = ArrowSprites(
    up=Skin.flick_arrow_up,
    up_left=Skin.flick_arrow_up_left,
    down=Skin.flick_arrow_down,
    down_left=Skin.flick_arrow_down_left,
    fallback=Skin.flick_arrow_fallback,
)
critical_arrow_sprites = ArrowSprites(
    up=Skin.critical_arrow_up,
    up_left=Skin.critical_arrow_up_left,
    down=Skin.critical_arrow_down,
    down_left=Skin.critical_arrow_down_left,
    fallback=Skin.critical_arrow_fallback,
)

normal_tick_sprites = TickSprites(
    normal=Skin.normal_slide_tick_note,
    fallback=Skin.normal_slide_tick_note_fallback,
)
slide_tick_sprites = normal_tick_sprites
critical_tick_sprites = TickSprites(
    normal=Skin.critical_slide_tick_note,
    fallback=Skin.critical_slide_tick_note_fallback,
)
normal_trace_tick_sprites = TickSprites(
    normal=Skin.normal_trace_tick_note,
    fallback=Skin.normal_trace_tick_note_fallback,
)
critical_trace_tick_sprites = TickSprites(
    normal=Skin.critical_trace_tick_note,
    fallback=Skin.critical_trace_tick_note_fallback,
)
trace_flick_tick_sprites = TickSprites(
    normal=Skin.trace_flick_tick_note,
    fallback=Skin.trace_flick_tick_note_fallback,
)

normal_slide_connector_sprites = ActiveConnectorSprites(
    normal=Skin.normal_slide_connector_normal,
    active=Skin.normal_slide_connector_active,
    fallback=Skin.normal_slide_connector_fallback,
)
critical_slide_connector_sprites = ActiveConnectorSprites(
    normal=Skin.critical_slide_connector_normal,
    active=Skin.critical_slide_connector_active,
    fallback=Skin.critical_slide_connector_fallback,
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
combo_label = ComboLabelSprite(
    normal=Skin.combo_label,
    ap=Skin.ap_combo_label,
    glow=Skin.combo_label_glow
)
judgment_text = JudgmentSprite(
    perfect=Skin.perfect,
    great=Skin.great,
    good=Skin.good,
    bad=Skin.bad,
    miss=Skin.miss,
    auto=Skin.auto
)
accuracy_text = AccuracySprite(
    fast=Skin.fast_warning,
    late=Skin.late_warning,
    flick=Skin.flick_warning,
)
damage_flash = DamageFlashSprite(
    normal=Skin.damage_flash
)