from sonolus.script.archetype import PlayArchetype, entity_memory
from sonolus.script.globals import level_memory

from sekai.lib import archetype_names
from sonolus.script.bucket import Judgment, JudgmentWindow
from sonolus.script.debug import debug_log, error
from sekai.lib.skin import combo_label, combo_number, judgment_text, accuracy_text, damage_flash

from sekai.lib.custom_elements import (
    draw_combo_label,
    draw_combo_number,
    draw_judgment_text,
    draw_judgment_accuracy,
    draw_damage_flash,
)
from sekai.lib.options import Options
from sonolus.script.runtime import time
from sonolus.script.interval import Interval


def spawn_custom(
    judgment: Judgment, accuracy: float, windows: JudgmentWindow, windows_bad: Interval, wrong_way: bool, check_pass: bool
):
    if Options.hide_custom == False:
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
            and judgment != Judgment.MISS
        ):
            JudgmentAccuracy.spawn(
                spawn_time=time(),
                judgment=judgment,
                accuracy=accuracy,
                windows=windows,
                wrong_way=wrong_way,
            )
        if Options.custom_damage and damage_flash.custom_available and Judgment.MISS:
            DamageFlash.spawn(spawn_time=time())


@level_memory
class comboLabel:
    ap: bool
    comboCheck: int


class ComboLabel(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.COMBO_LABEL

    def update_parallel(self):
        if self.combo != comboLabel.comboCheck:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_label(draw_time=self.spawn_time, ap=comboLabel.ap)

    def update_sequential(self):
        if self.check == True:
            return
        self.check = True
        if self.judgment == Judgment.MISS or self.judgment == Judgment.GOOD:
            comboLabel.comboCheck = 0
            self.combo = comboLabel.comboCheck
        else:
            comboLabel.comboCheck += 1
            self.combo = comboLabel.comboCheck
        if self.judgment != Judgment.PERFECT:
            comboLabel.ap = True


@level_memory
class comboNumber:
    ap: bool
    comboCheck: int


class ComboNumber(PlayArchetype):
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.COMBO_NUMBER

    def update_parallel(self):
        if self.combo != comboNumber.comboCheck:
            self.despawn = True
            return
        if self.combo == 0:
            self.despawn = True
            return
        draw_combo_number(
            draw_time=self.spawn_time, ap=comboNumber.ap, combo=self.combo
        )

    def update_sequential(self):
        if self.check == True:
            return
        self.check = True
        if self.judgment == Judgment.MISS or self.judgment == Judgment.GOOD:
            comboNumber.comboCheck = 0
            self.combo = comboNumber.comboCheck
        else:
            comboNumber.comboCheck += 1
            self.combo = comboNumber.comboCheck
        if self.judgment != Judgment.PERFECT:
            comboNumber.ap = True


@level_memory
class judgmentText:
    comboCheck: int


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
        if self.combo != judgmentText.comboCheck:
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
            check_pass=self.check_pass
        )

    def update_sequential(self):
        if self.check == True:
            return
        self.check = True
        judgmentText.comboCheck += 1
        self.combo = judgmentText.comboCheck


@level_memory
class judgmentAccuracy:
    comboCheck: int


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
        if self.combo != judgmentAccuracy.comboCheck:
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
        if self.check == True:
            return
        self.check = True
        judgmentAccuracy.comboCheck += 1
        self.combo = judgmentAccuracy.comboCheck


@level_memory
class damageFlash:
    comboCheck: int


class DamageFlash(PlayArchetype):
    spawn_time: float = entity_memory()
    check: bool = entity_memory()
    combo: int = entity_memory()
    name = archetype_names.DAMAGE_FLASH

    def update_parallel(self):
        if self.combo != damageFlash.comboCheck:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.35:
            self.despawn = True
            return
        draw_damage_flash(
            draw_time=self.spawn_time,
        )

    def update_sequential(self):
        if self.check == True:
            return
        self.check = True
        damageFlash.comboCheck += 1
        self.combo = damageFlash.comboCheck


CUSTOM_ARCHETYPES = (
    ComboLabel,
    ComboNumber,
    JudgmentText,
    JudgmentAccuracy,
    DamageFlash,
)
