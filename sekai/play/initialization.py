from sonolus.script.archetype import PlayArchetype, callback

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.note import init_note_life, init_score
from sekai.lib.ui import init_ui
from sekai.play.input_manager import InputManager
from sekai.play.note import NOTE_ARCHETYPES
from sekai.play.stage import Stage


class Initialization(PlayArchetype):
    name = archetype_names.INITIALIZATION

    @callback(order=-1)
    def preprocess(self):
        init_layout()
        init_ui()
        init_buckets()
        init_score()

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
