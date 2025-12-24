from sonolus.script.archetype import PlayArchetype, callback, entity_memory
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
from sekai.play import initialization
from sekai.play.events import Fever


def spawn_custom(
    judgment: Judgment,
    accuracy: float,
    windows: JudgmentWindow,
    windows_bad: Interval,
    wrong_way: bool,
    check_pass: bool,
    target_time: float,
):
    ComboJudge.spawn(
        target_time=target_time,
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
class ComboJudgeMemory:
    ap: bool
    combo_check: int
    latest_judge_id: int


class ComboJudge(PlayArchetype):
    target_time: float = entity_memory()
    spawn_time: float = entity_memory()
    judgment: Judgment = entity_memory()
    accuracy: Judgment = entity_memory()
    windows: JudgmentWindow = entity_memory()
    windows_bad: Interval = entity_memory()
    wrong_way: bool = entity_memory()
    check_pass: bool = entity_memory()
    my_judge_id: int = entity_memory()

    check: bool = entity_memory()
    combo: int = entity_memory()
    z: float = entity_memory()
    z1: float = entity_memory()
    z2: float = entity_memory()
    name = archetype_names.COMBO_JUDGE

    def initialize(self):
        self.z = initialization.LayerCache.judgment
        self.z1 = initialization.LayerCache.judgment1
        self.z2 = initialization.LayerCache.judgment2

    def update_parallel(self):
        if self.my_judge_id != ComboJudgeMemory.latest_judge_id:
            self.despawn = True
            return
        if self.combo != ComboJudgeMemory.combo_check:
            self.despawn = True
            return
        draw_combo_label(ap=ComboJudgeMemory.ap, z=self.z, z1=self.z1, combo=self.combo)
        draw_combo_number(
            draw_time=self.spawn_time, ap=ComboJudgeMemory.ap, combo=self.combo, z=self.z, z1=self.z1, z2=self.z2
        )
        draw_judgment_text(
            draw_time=self.spawn_time,
            judgment=self.judgment,
            windows_bad=self.windows_bad,
            accuracy=self.accuracy,
            check_pass=self.check_pass,
            z=self.z,
        )

    @callback(order=3)
    def update_sequential(self):
        if self.check:
            return
        self.check = True
        ComboJudgeMemory.latest_judge_id += 1
        self.my_judge_id = ComboJudgeMemory.latest_judge_id
        if self.judgment in (Judgment.MISS, Judgment.GOOD):
            ComboJudgeMemory.combo_check = 0
            self.combo = ComboJudgeMemory.combo_check
        else:
            ComboJudgeMemory.combo_check += 1
            self.combo = ComboJudgeMemory.combo_check
        if self.judgment != Judgment.PERFECT:
            ComboJudgeMemory.ap = True

        self.check_fever_count()

    def check_fever_count(self):
        if Fever.fever_chance_time <= self.target_time < Fever.fever_start_time:
            if self.judgment in (Judgment.MISS, Judgment.GOOD):
                Fever.fever_chance_cant_super_fever = True
            else:
                Fever.fever_chance_current_combo += 1


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
        self.z = initialization.LayerCache.judgment

    def update_parallel(self):
        if self.combo != JudgmentAccuracyMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.5:
            self.despawn = True
            return
        if not Options.custom_accuracy:
            self.despawn = True
            return
        draw_judgment_accuracy(
            judgment=self.judgment,
            accuracy=self.accuracy,
            windows=self.windows,
            wrong_way=self.wrong_way,
            z=self.z,
        )

    @callback(order=3)
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
        self.z = initialization.LayerCache.damage

    def update_parallel(self):
        if self.combo != DamageFlashMemory.combo_check:
            self.despawn = True
            return
        if time() >= self.spawn_time + 0.35:
            self.despawn = True
            return
        if not Options.custom_damage:
            self.despawn = True
            return
        draw_damage_flash(draw_time=self.spawn_time, z=self.z)

    @callback(order=3)
    def update_sequential(self):
        if self.check:
            return
        self.check = True
        DamageFlashMemory.combo_check += 1
        self.combo = DamageFlashMemory.combo_check


CUSTOM_ARCHETYPES = (
    ComboJudge,
    JudgmentAccuracy,
    DamageFlash,
)
