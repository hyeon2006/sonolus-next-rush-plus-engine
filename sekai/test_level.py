from sekai.level_utils import (
    LevelBpmChange,
    LevelCameraChange,
    LevelFeverChance,
    LevelFeverStart,
    LevelNote,
    LevelSkill,
    LevelSlide,
    LevelStage,
    LevelStageMaskChange,
    LevelStagePivotChange,
    LevelStageStyleChange,
    build_level,
)
from sekai.lib.connector import ConnectorKind
from sekai.lib.ease import EaseType
from sekai.lib.note import NoteKind
from sekai.lib.stage import DivisionParity, JudgeLineColor, StageBorderStyle

SLIDE_START_BEAT = 4.0
SLIDE_END_BEAT = 20.0
NUM_REGULAR_TICKS = 33  # head + 31 ticks + tail (~2 non-attached ticks/sec at BPM 60)
ATTACHED_PER_GAP = 3  # ~6 attached ticks/sec at BPM 60

STAGE_B_HALF_PERIOD_BEATS = 1.0  # 2-beat full back-and-forth = 2 seconds at BPM 60
STAGE_B_LANES = (-2.0, 5.0)
STAGE_B_END_BEAT = SLIDE_END_BEAT + 4.0


def _stage_b_oscillation_beats() -> list[float]:
    beats: list[float] = []
    beat = 0.0
    while beat <= STAGE_B_END_BEAT + 1e-6:
        beats.append(beat)
        beat += STAGE_B_HALF_PERIOD_BEATS
    return beats


stage_a = LevelStage(
    from_start=True,
    until_end=True,
    mask_changes=[
        LevelStageMaskChange(beat=0.0, lane=-5.0, size=1.0, ease=EaseType.LINEAR),
    ],
    pivot_changes=[
        LevelStagePivotChange(
            beat=0.0,
            lane=-5.0,
            division_size=1.0,
            division_parity=DivisionParity.EVEN,
            abs_y_offset=0.0,
            y_beat_offset=0.0,
            ease=EaseType.LINEAR,
        ),
    ],
    style_changes=[
        LevelStageStyleChange(
            beat=0.0,
            judge_line_color=JudgeLineColor.GREEN,
            left_border_style=StageBorderStyle.DEFAULT,
            right_border_style=StageBorderStyle.DEFAULT,
            alpha=1.0,
            lane_alpha=1.0,
            judge_line_alpha=1.0,
            ease=EaseType.LINEAR,
        ),
    ],
)

stage_b_mask_changes = [
    LevelStageMaskChange(
        beat=beat,
        lane=STAGE_B_LANES[i % 2],
        size=2.0,
        ease=EaseType.IN_OUT_QUAD,
    )
    for i, beat in enumerate(_stage_b_oscillation_beats())
]

stage_b_pivot_changes = [
    LevelStagePivotChange(
        beat=beat,
        lane=STAGE_B_LANES[i % 2],
        division_size=1.0,
        division_parity=DivisionParity.EVEN,
        abs_y_offset=0.0,
        y_beat_offset=0.0,
        ease=EaseType.IN_OUT_QUAD,
    )
    for i, beat in enumerate(_stage_b_oscillation_beats())
]

stage_b = LevelStage(
    from_start=True,
    until_end=True,
    mask_changes=stage_b_mask_changes,
    pivot_changes=stage_b_pivot_changes,
    style_changes=[
        LevelStageStyleChange(
            beat=0.0,
            judge_line_color=JudgeLineColor.PURPLE,
            left_border_style=StageBorderStyle.DEFAULT,
            right_border_style=StageBorderStyle.DEFAULT,
            alpha=1.0,
            lane_alpha=1.0,
            judge_line_alpha=1.0,
            ease=EaseType.LINEAR,
        ),
    ],
)

camera_changes = [
    LevelCameraChange(beat=0.0, lane=0.0, size=6.0, ease=EaseType.LINEAR),
]

regular_beats = [
    SLIDE_START_BEAT + i * (SLIDE_END_BEAT - SLIDE_START_BEAT) / (NUM_REGULAR_TICKS - 1)
    for i in range(NUM_REGULAR_TICKS)
]

slide = LevelSlide()
slide_notes: list[LevelNote] = []
attached_notes: list[LevelNote] = []

for i, beat in enumerate(regular_beats):
    is_first = i == 0
    is_last = i == NUM_REGULAR_TICKS - 1
    stage = stage_a if i % 2 == 0 else stage_b
    size = 1 if i % 2 == 0 else 2
    if is_first:
        kind = NoteKind.NORM_HEAD_TAP
    elif is_last:
        kind = NoteKind.NORM_TAIL_TAP
    else:
        kind = NoteKind.NORM_TICK
    slide_notes.append(
        LevelNote(
            beat=beat,
            lane=0.0,
            size=size,
            kind=kind,
            stage=stage,
            is_separator=is_first or is_last,
            segment_kind=ConnectorKind.ACTIVE_NORMAL,
            connector_ease=EaseType.IN_OUT_QUAD,
        )
    )
    if not is_last:
        next_beat = regular_beats[i + 1]
        for j in range(1, ATTACHED_PER_GAP + 1):
            frac = j / (ATTACHED_PER_GAP + 1)
            attached_notes.append(
                LevelNote(
                    beat=beat + frac * (next_beat - beat),
                    lane=0.0,
                    size=0.0,
                    kind=NoteKind.NORM_TICK,
                    stage=None,
                    attach=slide,
                )
            )

slide.notes = slide_notes


STAGE_A_PIVOT_LANE = -5.0


def _ease_in_out_quad(x: float) -> float:
    x = max(0.0, min(1.0, x))
    if x < 0.5:
        return 2 * x * x
    return 1 - 2 * (1 - x) ** 2


def _stage_b_pivot_at_beat(beat: float) -> float:
    pivot_beats = _stage_b_oscillation_beats()
    pivot_lanes = [STAGE_B_LANES[i % 2] for i in range(len(pivot_beats))]
    if beat <= pivot_beats[0]:
        return pivot_lanes[0]
    if beat >= pivot_beats[-1]:
        return pivot_lanes[-1]
    for i in range(len(pivot_beats) - 1):
        t_a = pivot_beats[i]
        t_b = pivot_beats[i + 1]
        if t_a <= beat <= t_b:
            frac = (beat - t_a) / (t_b - t_a)
            return pivot_lanes[i] + (pivot_lanes[i + 1] - pivot_lanes[i]) * _ease_in_out_quad(frac)
    return pivot_lanes[-1]


def _slide_abs_lane(i: int) -> float:
    if i % 2 == 0:
        return STAGE_A_PIVOT_LANE
    return _stage_b_pivot_at_beat(regular_beats[i])


guide_stage = LevelStage(
    from_start=True,
    until_end=True,
    pivot_changes=[
        LevelStagePivotChange(
            beat=0.0,
            lane=0.0,
            division_size=1.0,
            division_parity=DivisionParity.EVEN,
            abs_y_offset=0.0,
            y_beat_offset=0.0,
            ease=EaseType.LINEAR,
        ),
    ],
)

guide_slide = LevelSlide()
guide_slide.notes = [
    LevelNote(
        beat=beat,
        lane=_slide_abs_lane(i),
        size=1.0 if i % 2 == 0 else 2.0,
        kind=NoteKind.ANCHOR,
        stage=guide_stage,
        is_separator=True,
        segment_kind=ConnectorKind.GUIDE_RED,
        connector_ease=EaseType.IN_OUT_QUAD,
    )
    for i, beat in enumerate(regular_beats)
]

fever_chance = LevelFeverChance(beat=1.0, force=True)
fever_start = LevelFeverStart(beat=100)
test_skill = LevelSkill(beat=1.0, effect=2)


entities = [
    LevelBpmChange(beat=0.0, bpm=60.0),
    stage_a,
    stage_b,
    guide_stage,
    *camera_changes,
    slide,
    guide_slide,
    fever_chance,
    fever_start,
    test_skill,
    *attached_notes,
]

level = build_level(
    name="test",
    title="Test",
    bgm=None,
    entities=entities,
)


def load_levels():
    yield level
