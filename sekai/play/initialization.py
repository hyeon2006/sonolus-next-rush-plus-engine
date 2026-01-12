from sonolus.script.archetype import PlayArchetype, callback, imported

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.level_config import init_level_config
from sekai.lib.note import init_life, init_score
from sekai.lib.options import ConcreteScoreMode, ScoreMode
from sekai.lib.particle import init_particles
from sekai.lib.skin import init_skin
from sekai.lib.ui import init_ui
from sekai.play.input_manager import InputManager
from sekai.play.note import NOTE_ARCHETYPES
from sekai.play.stage import Stage


class Initialization(PlayArchetype):
    name = archetype_names.INITIALIZATION

    score_mode: ConcreteScoreMode = imported(name="scoreMode", default=ScoreMode.UNWEIGHTED_COMBO)
    initial_life: int = imported(name="initialLife", default=1000)

    @callback(order=-1)
    def preprocess(self):
        init_level_config(self.score_mode)
        init_layout()
        init_skin()
        init_particles()
        init_ui()
        init_buckets()
        init_score(NOTE_ARCHETYPES)
        init_life(NOTE_ARCHETYPES, self.initial_life)

    def initialize(self):
        Stage.spawn()
        InputManager.spawn()

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    def update_parallel(self):
        self.despawn = True
