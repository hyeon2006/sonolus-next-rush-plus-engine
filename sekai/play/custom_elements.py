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
from sekai.lib.options import Options
from sekai.lib.skin import accuracy_text, combo_label, combo_number, damage_flash, judgment_text


def spawn_custom(
    judgment: Judgment,
    accuracy: float,
    windows: JudgmentWindow,
    windows_bad: Interval,
    wrong_way: bool,
    check_pass: bool,
):
    if Options.hide_custom:
        return
    if Options.custom_combo and combo_label.custom_available:
        ComboLabel.spawn(spawn_time=time(), judgment=judgment)
    if Options.custom_combo and combo_number.custom_available:
        ComboNumber.spawn(spawn_time=time(), judgment=judgment)
    if Options.custom_judgment and judgment_text.custom_available:
        JudgmentText.spawn(
            spawn_time=time(),
            judgment=judgment,
            windows_bad=windows_bad,
            accuracy=accuracy,
            check_pass=check_pass,
        )
    if (
        Options.custom_judgment
        and Options.custom_accuracy
        and judgment_text.custom_available
        and accuracy_text.custom_available
        and judgment != Judgment.PERFECT
        and check_pass
    ):
        JudgmentAccuracy.spawn(
            spawn_time=time(),
            judgment=judgment,
            accuracy=accuracy,
            windows=windows,
            wrong_way=wrong_way,
        )
    if Options.custom_damage and damage_flash.custom_available and judgment == Judgment.MISS:
        DamageFlash.spawn(spawn_time=time())


@level_memory
class ComboLabelMemory:
    ap: bool
    combo_check: int


class ComboLabel(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.COMBO_LABEL

    def update_parallel(self):
        if self.combo != ComboLabelMemory.combo_check:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_label(draw_time=self.spawn_time, ap=ComboLabelMemory.ap)

    def update_sequential(self):
        if self.check:
            return
        self.check = True
        if self.judgment in (Judgment.MISS, Judgment.GOOD):
            ComboLabelMemory.combo_check = 0
            self.combo = ComboLabelMemory.combo_check
        else:
            ComboLabelMemory.combo_check += 1
            self.combo = ComboLabelMemory.combo_check
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
    name = archetype_names.COMBO_NUMBER

    def update_parallel(self):
        if self.combo != ComboNumberMemory.combo_check:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_number(draw_time=self.spawn_time, ap=ComboNumberMemory.ap, combo=self.combo)

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
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.JUDGMENT_TEXT

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
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.JUDGMENT_ACCURACY

    def update_parallel(self):
        if self.combo != JudgmentAccuracyMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.5:
            self.despawn = True
            return
        draw_judgment_accuracy(
            draw_time=self.spawn_time,
            judgment=self.judgment,
            accuracy=self.accuracy,
            windows=self.windows,
            wrong_way=self.wrong_way,
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
    name = archetype_names.DAMAGE_FLASH

    def update_parallel(self):
        if self.combo != DamageFlashMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.35:
            self.despawn = True
            return
        draw_damage_flash(
            draw_time=self.spawn_time,
        )

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
