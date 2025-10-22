from sonolus.script.archetype import EntityRef, WatchArchetype, entity_memory

from sekai.lib import archetype_names
from sekai.lib.custom_elements import (
    draw_combo_label,
    draw_combo_number,
    draw_damage_flash,
    draw_judgment_accuracy,
    draw_judgment_text,
)
from sekai.watch.note import WatchBaseNote


class ComboLabel(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    index: float = entity_memory()
    name = archetype_names.COMBO_LABEL

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0:
            return self.next_ref.get().hit_time
        else:
            return 1e8

    def update_parallel(self):
        if WatchBaseNote.at(self.index).combo == 0:
            return
        draw_combo_label(draw_time=self.spawn_time(), ap=WatchBaseNote.at(self.index).ap)


class ComboNumber(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    index: float = entity_memory()
    name = archetype_names.COMBO_NUMBER

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0:
            return self.next_ref.get().hit_time
        else:
            return 1e8

    def update_parallel(self):
        if WatchBaseNote.at(self.index).combo == 0:
            return
        draw_combo_number(
            draw_time=self.spawn_time(), ap=WatchBaseNote.at(self.index).ap, combo=WatchBaseNote.at(self.index).combo
        )


class JudgmentText(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    index: float = entity_memory()
    name = archetype_names.JUDGMENT_TEXT

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0 and WatchBaseNote.at(self.index).hit_time + 0.5 >= self.next_ref.get().hit_time:
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.index).hit_time + 0.5

    def update_parallel(self):
        draw_judgment_text(
            draw_time=self.spawn_time(),
            judgment=WatchBaseNote.at(self.index).judgment,
            windows_bad=WatchBaseNote.at(self.index).judgment_window_bad,
            accuracy=WatchBaseNote.at(self.index).accuracy,
            check_pass=WatchBaseNote.at(self.index).played_hit_effects,
        )


class JudgmentAccuracy(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    index: float = entity_memory()
    name = archetype_names.JUDGMENT_ACCURACY

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0 and WatchBaseNote.at(self.index).hit_time + 0.5 >= self.next_ref.get().hit_time:
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.index).hit_time + 0.5

    def update_parallel(self):
        draw_judgment_accuracy(
            draw_time=self.spawn_time(),
            judgment=WatchBaseNote.at(self.index).judgment,
            windows=WatchBaseNote.at(self.index).judgment_window,
            accuracy=WatchBaseNote.at(self.index).accuracy,
            wrong_way=WatchBaseNote.at(self.index).wrong_way_check,
        )


class DamageFlash(WatchArchetype):
    next_ref: EntityRef[WatchBaseNote] = entity_memory()
    index: float = entity_memory()
    name = archetype_names.DAMAGE_FLASH

    def spawn_time(self) -> float:
        return WatchBaseNote.at(self.index).hit_time

    def despawn_time(self):
        if self.next_ref.index > 0 and WatchBaseNote.at(self.index).hit_time + 0.35 >= self.next_ref.get().hit_time:
            return self.next_ref.get().hit_time
        else:
            return WatchBaseNote.at(self.index).hit_time + 0.35

    def update_parallel(self):
        draw_damage_flash(draw_time=self.spawn_time())


CUSTOM_ARCHETYPES = (ComboLabel, ComboNumber, JudgmentText, JudgmentAccuracy, DamageFlash)
