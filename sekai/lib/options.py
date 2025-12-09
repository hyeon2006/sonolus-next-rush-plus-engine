from sonolus.script.options import options, select_option, slider_option, toggle_option
from sonolus.script.text import StandardText


class ScoreMode(IntEnum):
    LEVEL_DEFAULT = 0
    WEIGHTED_FLAT = 1
    WEIGHTED_COMBO = 2
    UNWEIGHTED_FLAT = 3
    UNWEIGHTED_COMBO = 4


ConcreteScoreMode = Literal[
    ScoreMode.WEIGHTED_FLAT,
    ScoreMode.WEIGHTED_COMBO,
    ScoreMode.UNWEIGHTED_FLAT,
    ScoreMode.UNWEIGHTED_COMBO,
]


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
    note_effect_duration: float = slider_option(
        name="Effect Duration",
        scope="Sekai",
        default=1,
        min=0.1,
        max=1,
        step=0.05,
        unit=StandardText.PERCENTAGE_UNIT,
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
        values=["None", "Sonolus", "All"],
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
    version: int = select_option(
        name=StandardText.VERSION,
        description="The particle generation method, etc. will work with the selected version",
        scope="Rush",
        default=0,
        values=["v3", "v1"],
    )
    custom_combo: bool = toggle_option(
        name="Using Custom Combo",
        scope="Rush",
        default=True,
    )
    combo_distance: float = slider_option(
        name="Custom Combo Number Distance",
        scope="Rush",
        advanced=True,
        default=0.24,
        min=-0.5,
        max=0.5,
        step=0.01,
    )
    ap_effect: bool = toggle_option(
        name="AP Effect",
        scope="Rush",
        default=True,
    )
    custom_judgment: bool = toggle_option(
        name="Using Custom Judgment",
        scope="Rush",
        default=True,
    )
    custom_accuracy: bool = toggle_option(
        name="Late/Fast/Flick",
        scope="Rush",
        default=True,
    )
    auto_judgment: bool = toggle_option(
        name="Using Auto Judgment",
        description="When using Custom Judgment, judgment is always output as auto in Watch mode",
        scope="Rush",
        default=True,
    )
    custom_damage: bool = toggle_option(
        name="Using Custom Damage Effect",
        scope="Rush",
        default=True,
    )
    custom_tag: bool = toggle_option(
        name="Using Custom Tag",
        description="Play special tags like Auto Live while Watch mode",
        scope="Rush",
        default=True,
    )
    background_alpha: float = slider_option(
        name=StandardText.STAGE_ALPHA,
        scope="Sekai",
        default=1,
        min=0.5,
        max=1,
        step=0.1,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    lane_alpha: float = slider_option(
        name=StandardText.LANE_ALPHA,
        scope="Sekai",
        default=1,
        min=0,
        max=1,
        step=0.1,
        unit=StandardText.PERCENTAGE_UNIT,
    )
    fever_effect: int = select_option(
        name="Fever Effect",
        scope="Rush",
        default=0,
        values=["Default", "Lightweight", "None"],
    )
    forced_fever_chance: bool = toggle_option(
        name="Forced Fever Chance",
        description="Fever occurs even when not in a multiplayer environment",
        scope="Rush",
        default=False,
    )
    skill_effect: bool = toggle_option(
        name="Skill Effect",
        scope="Rush",
        default=True,
    )
