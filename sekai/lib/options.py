from enum import IntEnum

from sonolus.script.options import options, select_option, slider_option, toggle_option
from sonolus.script.text import StandardText


class ScoreMode(IntEnum):
    WEIGHTED_FLAT = 0
    WEIGHTED_COMBO = 1
    UNWEIGHTED_FLAT = 2
    UNWEIGHTED_COMBO = 3


class SkillMode(IntEnum):
    LEVEL_DEFAULT = 0
    SCORE = 1
    HEAL = 2
    JUDGMENT = 3

    @classmethod
    def from_options(cls, option_val: int, legacy_val: int) -> "SkillMode":
        if option_val == 1:
            return cls.SCORE
        if option_val == 2:
            return cls.HEAL
        if option_val == 3:
            return cls.JUDGMENT

        if legacy_val == 1:
            return cls.HEAL
        if legacy_val == 2:
            return cls.JUDGMENT

        return cls.SCORE


class SekaiVersion(IntEnum):
    v3 = 0
    v1 = 1


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
    skill_effect: bool = toggle_option(
        name="Skill Effect",
        scope="Rush",
        default=True,
    )
    sim_line_enabled: bool = toggle_option(
        name=StandardText.SIMLINE,
        scope="Sekai",
        default=True,
    )
    ap_effect: bool = toggle_option(
        name="AP Effect",
        scope="Rush",
        default=False,
    )
    custom_accuracy: bool = toggle_option(
        name="Late/Fast/Flick",
        scope="Rush",
        default=False,
    )
    mirror: bool = toggle_option(
        name=StandardText.MIRROR,
        default=False,
    )
    custom_combo: bool = toggle_option(
        name="Custom Combo",
        scope="Rush",
        default=True,
    )
    custom_score: int = select_option(
        name="Custom Score Indicator",
        scope="Rush",
        default=0,
        values=["Disable", "Arcade% (+)", "Arcade% (-)", "Accuracy%"],
    )
    combo_distance: float = slider_option(
        name="Custom Combo Number Distance",
        scope="Rush",
        advanced=True,
        default=0,
        min=-0.25,
        max=0.25,
        step=0.01,
    )
    custom_judgment: bool = toggle_option(
        name="Custom Judgment",
        scope="Rush",
        default=True,
    )
    auto_judgment: bool = toggle_option(
        name="Auto Judgment Display",
        description="Displays judgment as 'Auto' during Watch mode when Custom Judgment is enabled.",
        scope="Rush",
        default=True,
    )
    custom_damage: bool = toggle_option(
        name="Custom Damage Effect",
        scope="Rush",
        default=True,
    )
    custom_life_bar: bool = toggle_option(
        name="Custom Life Bar",
        scope="Rush",
        default=True,
    )
    custom_score_bar: bool = toggle_option(
        name="Custom Score Bar",
        scope="Rush",
        default=True,
    )
    custom_tag: bool = toggle_option(
        name="Custom Tag",
        description="Displays special tags (e.g., Auto Live) during Watch mode.",
        scope="Rush",
        default=True,
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
    connector_animation: bool = toggle_option(
        name=StandardText.CONNECTOR_ANIMATION,
        scope="Sekai",
        default=True,
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
        description="Custom UI does not support disabling this feature. If it crashes, please disable the conflicting settings.",
        default=True,
    )
    full_screen_ui: bool = toggle_option(
        name="Full Screen UI",
        scope="Rush",
        description="UI is displayed in full-screen aspect ratio.",
        advanced=True,
        default=False,
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
    forced_fever_chance: bool = toggle_option(
        name="Forced Fever Chance",
        description="Enables Fever Chance even in solo play.",
        scope="Rush",
        default=False,
    )
    skill_mode: SkillMode = select_option(
        name="Skill Mode",
        scope="Rush",
        values=[
            "Level Default",
            "Score Up",
            "Life Up",
            "Accuracy Up",
        ],
        standard=True,
        default=SkillMode.LEVEL_DEFAULT,
    )
    score_mode: ScoreMode = select_option(
        name="Score Mode",
        scope="Sekai",
        values=[
            "Weighted Flat",
            "Weighted Combo (Sekai Standard)",
            "Unweighted Flat (Sekai Rank Match)",
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
        "Custom Combo",
        "Custom Combo Number Distance",
        "Ap Effect",
        "Combo Judgment",
        "Late/Fast/Flick",
        "Auto Judgment",
        "Custom Damage Effect",
        "Custom Tag",
        StandardText.STAGE_ALPHA,
        StandardText.LANE_ALPHA,
        "Fever Effect",
        "Forced Fever Chance",
        "Skill Effect",
    )
