from sonolus.script.archetype import PlayArchetype, entity_memory
from sonolus.script.bucket import Judgment, JudgmentWindow
from sonolus.script.globals import level_memory
from sonolus.script.interval import Interval
from sonolus.script.runtime import time

from sekai.lib import archetype_names
from sekai.lib.custom_elements import (
    draw_combo_label,
    draw_combo_number,
    draw_damage_flash,
    draw_judgment_accuracy,
    draw_judgment_text,
)
from sekai.play import note


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


def spawn_custom(
    judgment: Judgment,
    accuracy: float,
    windows: JudgmentWindow,
    windows_bad: Interval,
    wrong_way: bool,
    check_pass: bool,
    target_time: float,
):
    ComboLabel.spawn(target_time=target_time, judgment=judgment)
    ComboNumber.spawn(spawn_time=time(), judgment=judgment)
    JudgmentText.spawn(
        spawn_time=time(),
        judgment=judgment,
        windows_bad=windows_bad,
        accuracy=accuracy,
        check_pass=check_pass,
    )
    if judgment != Judgment.PERFECT and check_pass:
        JudgmentAccuracy.spawn(
            spawn_time=time(),
            judgment=judgment,
            accuracy=accuracy,
            windows=windows,
            wrong_way=wrong_way,
        )
    if judgment == Judgment.MISS:
        DamageFlash.spawn(spawn_time=time())


@level_memory
class ComboLabelMemory:
    ap: bool
    combo_check: int


class ComboLabel(PlayArchetype):
    target_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    z: float = entity_memory()
    glow_z: float = entity_memory()
    name = archetype_names.COMBO_LABEL

    def initialize(self):
        self.z = PrecalcLayer.judgment1
        self.glow_z = PrecalcLayer.judgment

    def update_parallel(self):
        if self.combo != ComboLabelMemory.combo_check:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_label(ap=ComboLabelMemory.ap, z=self.z, glow_z=self.glow_z)

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        if self.judgment in (Judgment.MISS, Judgment.GOOD):
            ComboLabelMemory.combo_check = 0
            self.combo = ComboLabelMemory.combo_check
            if (
                note.FeverChanceEventCounter.fever_chance_time
                <= self.target_time
                < note.FeverChanceEventCounter.fever_start_time
            ):
                note.FeverChanceEventCounter.fever_chance_cant_super_fever = True
        else:
            ComboLabelMemory.combo_check += 1
            self.combo = ComboLabelMemory.combo_check
            if (
                note.FeverChanceEventCounter.fever_chance_time
                <= self.target_time
                < note.FeverChanceEventCounter.fever_start_time
            ):
                note.FeverChanceEventCounter.fever_chance_current_combo += 1
        if self.judgment != Judgment.PERFECT:
            ComboLabelMemory.ap = True


@level_memory
class ComboNumberMemory:
    ap: bool
    combo_check: int


class ComboNumber(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    z: float = entity_memory()
    z2: float = entity_memory()
    z3: float = entity_memory()
    name = archetype_names.COMBO_NUMBER

    def initialize(self):
        self.z = PrecalcLayer.judgment1
        self.z2 = PrecalcLayer.judgment
        self.z3 = PrecalcLayer.judgment2

    def update_parallel(self):
        if self.combo != ComboNumberMemory.combo_check:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_number(
            draw_time=self.spawn_time, ap=ComboNumberMemory.ap, combo=self.combo, z=self.z, z2=self.z2, z3=self.z3
        )

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        if self.judgment in (Judgment.MISS, Judgment.GOOD):
            ComboNumberMemory.combo_check = 0
            self.combo = ComboNumberMemory.combo_check
        else:
            ComboNumberMemory.combo_check += 1
            self.combo = ComboNumberMemory.combo_check
        if self.judgment != Judgment.PERFECT:
            ComboNumberMemory.ap = True


@level_memory
class JudgmentTextMemory:
    combo_check: int


class JudgmentText(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    accuracy: Judgment = entity_memory()
    windows_bad: Interval = entity_memory()
    check_pass: bool = entity_memory()
    z: float = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.JUDGMENT_TEXT

    def initialize(self):
        self.z = PrecalcLayer.judgment

    def update_parallel(self):
        if self.combo != JudgmentTextMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.5:
            self.despawn = True
            return
        draw_judgment_text(
            draw_time=self.spawn_time,
            judgment=self.judgment,
            windows_bad=self.windows_bad,
            accuracy=self.accuracy,
            check_pass=self.check_pass,
            z=self.z,
        )

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        JudgmentTextMemory.combo_check += 1
        self.combo = JudgmentTextMemory.combo_check


@level_memory
class JudgmentAccuracyMemory:
    combo_check: int


class JudgmentAccuracy(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    accuracy: float = entity_memory()
    windows: JudgmentWindow = entity_memory()
    wrong_way: bool = entity_memory()
    z: float = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.JUDGMENT_ACCURACY

    def initialize(self):
        self.z = PrecalcLayer.judgment

    def update_parallel(self):
        if self.combo != JudgmentAccuracyMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.5:
            self.despawn = True
            return
        draw_judgment_accuracy(
            judgment=self.judgment,
            accuracy=self.accuracy,
            windows=self.windows,
            wrong_way=self.wrong_way,
            z=self.z,
        )

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        JudgmentAccuracyMemory.combo_check += 1
        self.combo = JudgmentAccuracyMemory.combo_check


@level_memory
class DamageFlashMemory:
    combo_check: int


class DamageFlash(PlayArchetype):
    spawn_time: float = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    z: float = entity_memory()
    name = archetype_names.DAMAGE_FLASH

    def initialize(self):
        self.z = PrecalcLayer.damage

    def update_parallel(self):
        if self.combo != DamageFlashMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.35:
            self.despawn = True
            return
        draw_damage_flash(draw_time=self.spawn_time, z=self.z)

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        DamageFlashMemory.combo_check += 1
        self.combo = DamageFlashMemory.combo_check


CUSTOM_ARCHETYPES = (
    ComboLabel,
    ComboNumber,
    JudgmentText,
    JudgmentAccuracy,
    DamageFlash,
)
