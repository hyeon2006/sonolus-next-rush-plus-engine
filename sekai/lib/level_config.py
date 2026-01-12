from sonolus.script.globals import level_data

from sekai.lib.options import ConcreteScoreMode, Options, ScoreMode


@level_data
class LevelConfig:
    score_mode: ConcreteScoreMode


def init_level_config(
    level_score_mode: ConcreteScoreMode,
):
    score_mode_option = Options.score_mode
    if score_mode_option != ScoreMode.LEVEL_DEFAULT:
        LevelConfig.score_mode = score_mode_option
    else:
        LevelConfig.score_mode = level_score_mode
