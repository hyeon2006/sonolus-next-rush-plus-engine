from sonolus.script.archetype import PlayArchetype, callback, imported

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layer import LAYER_DAMAGE, LAYER_JUDGMENT, get_z
from sekai.lib.layout import init_layout
from sekai.lib.note import init_note_life, init_score
from sekai.lib.particle import init_particles
from sekai.lib.skin import init_skin
from sekai.lib.ui import init_ui
from sekai.play.custom_elements import PrecalcLayer
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
        init_score()

        PrecalcLayer.judgment = get_z(layer=LAYER_JUDGMENT)
        PrecalcLayer.judgment1 = get_z(layer=LAYER_JUDGMENT, etc=1)
        PrecalcLayer.judgment2 = get_z(layer=LAYER_JUDGMENT, etc=2)
        PrecalcLayer.damage = get_z(layer=LAYER_DAMAGE)

        for note_archetype in NOTE_ARCHETYPES:
            init_note_life(note_archetype)

    def initialize(self):
        Stage.spawn()
        InputManager.spawn()

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    def update_parallel(self):
        self.despawn = True
