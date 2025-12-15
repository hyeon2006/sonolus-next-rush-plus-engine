from sonolus.script.archetype import StandardImport, WatchArchetype, callback, entity_memory, imported
from sonolus.script.globals import level_memory
from sonolus.script.interval import clamp
from sonolus.script.runtime import is_replay, is_skip, time
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.effect import SFX_DISTANCE, Effects
from sekai.lib.events import (
    draw_fever_gauge,
    draw_fever_side_bar,
    draw_fever_side_cover,
    draw_skill_bar,
    spawn_fever_chance_particle,
    spawn_fever_start_particle,
)
from sekai.lib.options import Options
from sekai.lib.streams import Streams
from sekai.watch import custom_elements, note


@level_memory
class SkillMemory:
    max_count: int


class Skill(WatchArchetype):
    beat: StandardImport.BEAT
    start_time: float = entity_memory()
    name = archetype_names.SKILL
    z: float = entity_memory()
    z2: float = entity_memory()
    count: int = entity_memory()
    sfx: bool = entity_memory()

    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        self.z = custom_elements.PrecalcLayer.skill_bar
        self.z2 = custom_elements.PrecalcLayer.skill_etc
        Effects.skill.schedule(self.start_time, SFX_DISTANCE)

    def spawn_time(self):
        return self.start_time

    def despawn_time(self):
        return self.start_time + 3

    def update_parallel(self):
        if self.count == 0:
            self.count = SkillMemory.max_count
        if is_skip():
            self.sfx = False
        draw_skill_bar(self.z, self.z2, time() - self.start_time, self.count)

    @callback(order=3)
    def update_sequential(self):
        if self.count:
            return
        SkillMemory.max_count += 1


class FeverChance(WatchArchetype):
    beat: StandardImport.BEAT
    force: bool = imported(name="force")
    start_time: float = entity_memory()
    checker: int = entity_memory()
    counter: int = entity_memory()
    percentage: float = entity_memory()
    name = archetype_names.FEVER_CHANCE
    z: float = entity_memory()
    z2: float = entity_memory()
    z3: float = entity_memory()

    @callback(order=-2)
    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        note.FeverChanceEventCounter.fever_chance_time = (
            min(self.start_time, note.FeverChanceEventCounter.fever_chance_time)
            if note.FeverChanceEventCounter.fever_chance_time != 0
            else self.start_time
        )

    def initialize(self):
        self.z = custom_elements.PrecalcLayer.fever_chance_cover
        self.z2 = custom_elements.PrecalcLayer.fever_chance_side
        self.z3 = custom_elements.PrecalcLayer.fever_chance_gauge

    def spawn_time(self):
        return self.start_time

    def despawn_time(self):
        return note.FeverChanceEventCounter.fever_start_time + 10

    def update_parallel(self):
        if not is_replay() and not Options.forced_fever_chance and not self.force:
            return
        if is_skip():
            self.checker = 0
            if time() <= self.start_time:
                self.percentage = 0
        if self.checker >= 2:
            return
        if time() >= note.FeverChanceEventCounter.fever_start_time:
            if self.percentage >= 0.78:
                spawn_fever_start_particle(note.FeverChanceEventCounter.fever_chance_cant_super_fever)
            self.checker = 2
            return
        if time() >= note.FeverChanceEventCounter.fever_chance_time and not self.checker:
            spawn_fever_chance_particle()
            self.checker = 1
        self.percentage = (
            clamp(
                note.FeverChanceEventCounter.fever_chance_current_combo / self.counter,
                0,
                0.9 if not note.FeverChanceEventCounter.fever_chance_cant_super_fever else 0.89,
            )
            if not Streams.fever_chance_counter[0][-2]
            else Streams.fever_chance_counter[0][time()]
        )
        if Options.fever_effect == 0:
            draw_fever_side_cover(self.z, time() - self.start_time)
        draw_fever_side_bar(self.z2, time() - self.start_time)
        draw_fever_gauge(self.z3, self.percentage)

    @callback(order=3)
    def update_sequential(self):
        if self.checker:
            return
        self.counter = note.FeverChanceEventCounter.fever_last_count - note.FeverChanceEventCounter.fever_first_count

    def terminate(self):
        self.percentage = 0
        self.checker = 0


class FeverStart(WatchArchetype):
    beat: StandardImport.BEAT
    start_time: float = entity_memory()
    name = archetype_names.FEVER_START

    @callback(order=-2)
    def preprocess(self):
        self.start_time = beat_to_time(self.beat)
        note.FeverChanceEventCounter.fever_start_time = (
            min(self.start_time, note.FeverChanceEventCounter.fever_start_time)
            if note.FeverChanceEventCounter.fever_start_time != 0
            else self.start_time
        )

    def spawn_time(self):
        return 1e8

    def despawn_time(self):
        return 1e8


EVENT_ARCHETYPES = (Skill, FeverChance, FeverStart)
