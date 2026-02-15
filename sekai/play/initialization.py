from sonolus.script.archetype import PlayArchetype, callback, exported, imported

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.level_config import EngineRevision, init_level_config
from sekai.lib.note import init_life, init_score
from sekai.lib.particle import init_particles
from sekai.lib.skin import init_skin
from sekai.lib.ui import init_ui
from sekai.play.common import init_play_common
from sekai.play.input_manager import InputManager
from sekai.play.note import NOTE_ARCHETYPES
from sekai.play.stage import Stage


class Initialization(PlayArchetype):
    name = archetype_names.INITIALIZATION

    revision: EngineRevision = imported(name="revision", default=EngineRevision.SONOLUS_1_1_0)
    initial_life: int = imported(name="initialLife", default=1000)

    replay_revision: EngineRevision = exported(name="replayRevision")

    @callback(order=-1)
    def preprocess(self):
        init_level_config(self.revision)
        init_layout()
        init_skin()
        init_particles()
        init_ui()
        init_buckets()
        init_score(NOTE_ARCHETYPES)
        init_life(NOTE_ARCHETYPES, self.initial_life)
        init_play_common()

    def initialize(self):
        Stage.spawn()
        InputManager.spawn()
        self.replay_revision = self.revision

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    def update_parallel(self):
        self.despawn = True
