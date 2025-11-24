from sonolus.script.archetype import (
    PlayArchetype,
    StandardImport,
    callback,
    entity_memory,
)
from sonolus.script.interval import clamp
from sonolus.script.runtime import time
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.events import draw_fever_side_cover
from sekai.play import note


class Skill(PlayArchetype):
    beat: StandardImport.BEAT
    start_time: float = entity_memory()
    name = archetype_names.SKILL

    def preprocess(self):
        self.start_time = beat_to_time(self.beat)

    def spawn_order(self):
        return self.start_time

    def should_spawn(self):
        return time() >= self.start_time

    def update_parallel(self):
        self.despawn = True


class FeverChance(PlayArchetype):
    beat: StandardImport.BEAT
    start_time: float = entity_memory()
    checker: bool = entity_memory()
    counter: int = entity_memory()
    percentage: float = entity_memory()
    name = archetype_names.FEVER_CHANCE

    @callback(order=-2)
    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        note.FeverChanceEventCounter.fever_chance_time = self.start_time

    def spawn_order(self):
        return self.start_time

    def should_spawn(self):
        return time() >= self.start_time

    def update_parallel(self):
        if time() >= note.FeverChanceEventCounter.fever_start_time:
            self.despawn = True
            return
        draw_fever_side_cover()
        self.percentage = clamp(
            note.FeverChanceEventCounter.fever_chance_current_combo / self.counter,
            0,
            1 if not note.FeverChanceEventCounter.fever_chance_cant_super_fever else 0.99,
        )

    def update_sequential(self):
        if self.checker:
            return
        self.checker = True
        self.counter = (
            note.FeverChanceEventCounter.fever_last_note.get().count
            - note.FeverChanceEventCounter.fever_first_note.get().count
        )


class FeverStart(PlayArchetype):
    beat: StandardImport.BEAT
    start_time: float = entity_memory()
    name = archetype_names.FEVER_START

    @callback(order=-2)
    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        note.FeverChanceEventCounter.fever_start_time = self.start_time

    def spawn_order(self):
        return 1e8

    def should_spawn(self):
        return False


EVENT_ARCHETYPES = (Skill, FeverChance, FeverStart)
