from sonolus.script.archetype import (
    PlayArchetype,
    StandardImport,
    callback,
    entity_memory,
)
from sonolus.script.interval import clamp
from sonolus.script.runtime import is_multiplayer, time
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.events import (
    draw_fever_gauge,
    draw_fever_side_bar,
    draw_fever_side_cover,
    spawn_fever_start_particle,
)
from sekai.lib.options import Options
from sekai.play import custom_elements, note


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
    z: float = entity_memory()
    z2: float = entity_memory()
    z3: float = entity_memory()

    @callback(order=-2)
    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        note.FeverChanceEventCounter.fever_chance_time = self.start_time

    def initialize(self):
        self.z = custom_elements.PrecalcLayer.fever_chance_cover
        self.z2 = custom_elements.PrecalcLayer.fever_chance_side
        self.z3 = custom_elements.PrecalcLayer.fever_chance_gauge

    def spawn_order(self):
        return self.start_time

    def should_spawn(self):
        return time() >= self.start_time

    def update_parallel(self):
        if not is_multiplayer() and not Options.forced_fever_chance:
            self.despawn = True
            return
        if time() >= note.FeverChanceEventCounter.fever_start_time:
            spawn_fever_start_particle(
                note.FeverChanceEventCounter.fever_chance_cant_super_fever
            )
            self.despawn = True
            return
        self.checker = True
        self.percentage = clamp(
            note.FeverChanceEventCounter.fever_chance_current_combo / self.counter,
            0,
            0.9,
        )
        draw_fever_side_cover(self.z, time() - self.start_time)
        draw_fever_side_bar(self.z2, time() - self.start_time)
        draw_fever_gauge(self.z3, self.percentage)

    def update_sequential(self):
        if self.checker:
            return
        self.counter = (
            note.FeverChanceEventCounter.fever_last_count
            - note.FeverChanceEventCounter.fever_first_count
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
