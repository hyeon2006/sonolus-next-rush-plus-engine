from sonolus.script.archetype import PlayArchetype, entity_memory
from sonolus.script.globals import level_memory

from sekai.lib import archetype_names
from sonolus.script.bucket import Judgment
from sonolus.script.debug import debug_log
from sekai.lib.skin import combo_label, combo_number

from sekai.lib.custom_elements import draw_combo_label, draw_combo_number
from sekai.lib.options import Options
from sonolus.script.runtime import time

def spawn_custom(judgment):
    if Options.hide_custom == False:
        if Options.custom_combo and combo_label.custom_available:
            ComboLabel.spawn(
                spawn_time=time(),
                judgment=judgment
                )
        if Options.custom_combo and combo_number.custom_available:
            ComboNumber.spawn(
                spawn_time=time(),
                judgment=judgment
                )


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
        draw_combo_label(
            draw_time=self.spawn_time,
            ap=comboLabel.ap
        )
    
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
            draw_time=self.spawn_time,
            ap=comboNumber.ap,
            combo=self.combo
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


CUSTOM_ARCHETYPES = (
    ComboLabel,
    ComboNumber,
)