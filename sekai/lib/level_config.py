from enum import IntEnum

from sonolus.script.globals import level_data

from sekai.lib.options import ConcreteScoreMode, Options, ScoreMode, SekaiVersion


class EngineRevision(IntEnum):
    BASE = 0
    SONOLUS_1_1_0 = 1


@level_data
class LevelConfig:
    revision: EngineRevision
    score_mode: ConcreteScoreMode
    ui_version: SekaiVersion
    particle_version: SekaiVersion


def init_level_config(
    revision: EngineRevision = EngineRevision.SONOLUS_1_1_0,
):
    LevelConfig.revision = revision
    score_mode_option = Options.score_mode
    if score_mode_option != ScoreMode.LEVEL_DEFAULT:
        LevelConfig.score_mode = score_mode_option
    else:
        LevelConfig.score_mode = ScoreMode.UNWEIGHTED_FLAT


def init_ui_version(ui_version: SekaiVersion):
    LevelConfig.ui_version = ui_version


def init_particle_version(particle_version: SekaiVersion):
    LevelConfig.particle_version = particle_version
