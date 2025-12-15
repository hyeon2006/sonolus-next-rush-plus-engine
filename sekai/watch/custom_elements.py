from sonolus.script.archetype import EntityRef, WatchArchetype, callback, entity_memory
from sonolus.script.globals import level_memory

from sekai.lib import archetype_names
from sekai.lib.custom_elements import (
    draw_combo_label,
    draw_combo_number,
    draw_damage_flash,
    draw_judgment_accuracy,
    draw_judgment_text,
)
from sekai.watch import note
from sekai.watch.note import WatchBaseNote


@level_memory
class PrecalcLayer:
    judgment: float
    judgment1: float
    judgment2: float
    damage: float
    fever_chance_cover: float
    fever_chance_side: float
    fever_chance_gauge: float
    skill_bar: float
    skill_etc: float


class ComboLabel(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    note_index: int = entity_memory()
    z: float = entity_memory()
    checker: float = entity_memory()
    glow_z: float = entity_memory()
    name = archetype_names.COMBO_LABEL

    def initialize(self):
        self.z = PrecalcLayer.judgment1
        self.glow_z = PrecalcLayer.judgment

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.note_index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0:
            return self.next_ref.get().hit_time
        else:
            return 1e8

    def update_parallel(self):
        if WatchBaseNote.at(self.note_index).combo == 0:
            return
        draw_combo_label(ap=WatchBaseNote.at(self.note_index).ap, z=self.z, glow_z=self.glow_z)

    @callback(order=3)
    def update_sequential(self):
        if self.checker:
            return
        if (
            note.FeverChanceEventCounter.fever_chance_time
            <= WatchBaseNote.at(self.note_index).hit_time
            < note.FeverChanceEventCounter.fever_start_time
        ):
            note.FeverChanceEventCounter.fever_chance_current_combo = (
                WatchBaseNote.at(self.note_index).count - note.FeverChanceEventCounter.fever_first_count
            )
            self.checker = True

    def terminate(self):
        self.checker = False


class ComboNumber(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    note_index: int = entity_memory()
    z: float = entity_memory()
    z2: float = entity_memory()
    z3: float = entity_memory()
    name = archetype_names.COMBO_NUMBER

    def initialize(self):
        self.z = PrecalcLayer.judgment1
        self.z2 = PrecalcLayer.judgment
        self.z3 = PrecalcLayer.judgment2

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.note_index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0:
            return self.next_ref.get().hit_time
        else:
            return 1e8

    def update_parallel(self):
        if WatchBaseNote.at(self.note_index).combo == 0:
            return
        draw_combo_number(
            draw_time=self.spawn_time(),
            ap=WatchBaseNote.at(self.note_index).ap,
            combo=WatchBaseNote.at(self.note_index).combo,
            z=self.z,
            z2=self.z2,
            z3=self.z3,
        )


class JudgmentText(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    note_index: int = entity_memory()
    z: float = entity_memory()
    name = archetype_names.JUDGMENT_TEXT

    def initialize(self):
        self.z = PrecalcLayer.judgment

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.note_index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0 and WatchBaseNote.at(self.note_index).hit_time + 0.5 >= self.next_ref.get().hit_time:
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.note_index).hit_time + 0.5

    def update_parallel(self):
        draw_judgment_text(
            draw_time=self.spawn_time(),
            judgment=WatchBaseNote.at(self.note_index).judgment,
            windows_bad=WatchBaseNote.at(self.note_index).judgment_window_bad,
            accuracy=WatchBaseNote.at(self.note_index).accuracy,
            check_pass=WatchBaseNote.at(self.note_index).played_hit_effects,
            z=self.z,
        )


class JudgmentAccuracy(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    note_index: int = entity_memory()
    z: float = entity_memory()
    name = archetype_names.JUDGMENT_ACCURACY

    def initialize(self):
        self.z = PrecalcLayer.judgment

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.note_index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0 and WatchBaseNote.at(self.note_index).hit_time + 0.5 >= self.next_ref.get().hit_time:
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.note_index).hit_time + 0.5

    def update_parallel(self):
        draw_judgment_accuracy(
            judgment=WatchBaseNote.at(self.note_index).judgment,
            windows=WatchBaseNote.at(self.note_index).judgment_window,
            accuracy=WatchBaseNote.at(self.note_index).accuracy,
            wrong_way=WatchBaseNote.at(self.note_index).wrong_way_check,
            z=self.z,
        )


class DamageFlash(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    note_index: int = entity_memory()
    z: float = entity_memory()
    name = archetype_names.DAMAGE_FLASH

    def initialize(self):
        self.z = PrecalcLayer.damage

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.note_index).hit_time

    def despawn_time(self):
        if (
            self.next_ref.index > 0
            and WatchBaseNote.at(self.note_index).hit_time + 0.35 >= self.next_ref.get().hit_time
        ):
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.note_index).hit_time + 0.35

    def update_parallel(self):
        draw_damage_flash(draw_time=self.spawn_time(), z=self.z)


CUSTOM_ARCHETYPES = (ComboLabel, ComboNumber, JudgmentText, JudgmentAccuracy, DamageFlash)
