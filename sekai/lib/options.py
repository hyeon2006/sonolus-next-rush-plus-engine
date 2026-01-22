from enum import IntEnum

from sonolus.script.options import options, select_option, slider_option, toggle_option
from sonolus.script.text import StandardText


class ScoreMode(IntEnum):
    WEIGHTED_FLAT = 0
    WEIGHTED_COMBO = 1
    UNWEIGHTED_FLAT = 2
    UNWEIGHTED_COMBO = 3


@options
class Options:
    speed: float = slider_option(
        name=StandardText.SPEED,
        standard=True,
        advanced=True,
        default=1,
        min=0.5,
        max=2,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    note_speed: float = slider_option(
        name=StandardText.NOTE_SPEED,
        scope="Sekai",
        default=6,
        min=1,
        max=12,
        step=0.01,
    )
    mirror: bool = toggle_option(
        name=StandardText.MIRROR,
        default=False,
    )
    sfx_enabled: bool = toggle_option(
        name=StandardText.EFFECT,
        scope="Sekai",
        default=True,
    )
    auto_sfx: bool = toggle_option(
        name=StandardText.EFFECT_AUTO,
        scope="Sekai",
        default=False,
    )
    haptics_enabled: bool = toggle_option(
        name=StandardText.HAPTIC,
        scope="Sekai",
        default=False,
    )
    note_effect_enabled: bool = toggle_option(
        name=StandardText.NOTE_EFFECT,
        scope="Sekai",
        default=True,
    )
    note_effect_size: float = slider_option(
        name=StandardText.NOTE_EFFECT_SIZE,
        scope="Sekai",
        default=1,
        min=0.1,
        max=2,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    marker_animation: bool = toggle_option(
        name=StandardText.MARKER_ANIMATION,
        scope="Sekai",
        default=True,
    )
    sim_line_enabled: bool = toggle_option(
        name=StandardText.SIMLINE,
        scope="Sekai",
        default=True,
    )
    connector_animation: bool = toggle_option(
        name=StandardText.CONNECTOR_ANIMATION,
        scope="Sekai",
        default=True,
    )
    slide_alpha: float = slider_option(
        name="Slide Alpha",
        scope="Sekai",
        default=1,
        min=0,
        max=1,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    guide_alpha: float = slider_option(
        name="Guide Alpha",
        scope="Sekai",
        default=0.6,
        min=0,
        max=1,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    lane_effect_enabled: bool = toggle_option(
        name=StandardText.LANE_EFFECT,
        scope="Sekai",
        default=True,
    )
    slot_effect_enabled: bool = toggle_option(
        name=StandardText.SLOT_EFFECT,
        scope="Sekai",
        default=True,
    )
    slot_effect_size: float = slider_option(
        name=StandardText.SLOT_EFFECT_SIZE,
        scope="Sekai",
        default=1,
        min=0,
        max=2,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    stage_cover: float = slider_option(
        name=StandardText.STAGE_COVER_VERTICAL,
        advanced=True,
        scope="Sekai",
        default=0,
        min=0,
        max=1,
        step=0.01,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    hidden: float = slider_option(
        name=StandardText.HIDDEN,
        scope="Sekai",
        advanced=True,
        default=0,
        min=0,
        max=1,
        step=0.01,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    lock_stage_aspect_ratio: bool = toggle_option(
        name=StandardText.STAGE_ASPECTRATIO_LOCK,
        scope="Sekai",
        default=True,
    )
    hide_ui: int = select_option(
        name="Hide UI",
        scope="Rush",
        default=0,
        values=["None", "Sonolus", "Sonolus + Custom Judgment", "All"],
    )
    show_lane: bool = toggle_option(
        name=StandardText.STAGE,
        scope="Sekai",
        default=True,
    )
    slide_quality: float = slider_option(
        name="Slide Quality",
        scope="Next Sekai",
        default=1,
        min=0.5,
        max=2,
        step=0.1,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    guide_quality: float = slider_option(
        name="Guide Quality",
        scope="Next Sekai",
        default=1,
        min=0.5,
        max=2,
        step=0.1,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    note_margin: float = slider_option(
        name="Note Margin",
        scope="Next Sekai",
        default=0.0,
        min=0.0,
        max=0.2,
        step=0.01,
    )
    effect_animation_speed: float = slider_option(
        name="Effect Animation Speed",
        scope="Next Sekai",
        default=1,
        min=0.25,
        max=4,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    alternative_approach_curve: bool = toggle_option(
        name="Alternative Approach Curve",
        advanced=True,
        default=False,
        scope="Next Sekai",
    )
    disable_timescale: bool = toggle_option(
        name="Disable Timescale",
        standard=True,
        advanced=True,
        default=False,
    )
    disable_fake_notes: bool = toggle_option(
        name="Disable Fake Notes",
        standard=True,
        advanced=True,
        default=False,
    )
    score_mode: ScoreMode = select_option(
        name="Score Mode",
        scope="Sekai",
        values=[
            "Weighted Flat",
            "Weighted Combo (Sekai Standard)",
            "Unweighted Flat (Sekai Ranked Match)",
            "Unweighted Combo",
        ],
        standard=True,
        advanced=True,
        default=1,
    )

    replay_fallback_option_names = (
        StandardText.SPEED,
        StandardText.NOTE_SPEED,
        StandardText.MIRROR,
        StandardText.EFFECT,
        StandardText.EFFECT_AUTO,
        StandardText.NOTE_EFFECT,
        StandardText.NOTE_EFFECT_SIZE,
        StandardText.MARKER_ANIMATION,
        StandardText.SIMLINE,
        StandardText.CONNECTOR_ANIMATION,
        "Slide Alpha",
        "Guide Alpha",
        StandardText.LANE_EFFECT,
        StandardText.SLOT_EFFECT,
        StandardText.SLOT_EFFECT_SIZE,
        StandardText.STAGE_COVER_VERTICAL,
        StandardText.HIDDEN,
        StandardText.STAGE_ASPECTRATIO_LOCK,
        "Hide UI",
        StandardText.STAGE,
        "Slide Quality",
        "Guide Quality",
        "Note Margin",
        "Alternative Approach Curve",
        "Disable Timescale",
        StandardText.VERSION,
        "Using Custom Combo",
        "Custom Combo Number Distance",
        "Ap Effect",
        "Using Combo Judgment",
        "Late/Fast/Flick",
        "Using Auto Judgment",
        "Using Custom Damage Effect",
        "Using Custom Tag",
        StandardText.STAGE_ALPHA,
        StandardText.LANE_ALPHA,
        "Fever Effect",
        "Forced Fever Chance",
        "Skill Effect",
    )
