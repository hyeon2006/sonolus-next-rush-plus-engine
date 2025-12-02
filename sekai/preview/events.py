from sonolus.script.archetype import PreviewArchetype, StandardImport, entity_data, imported
from sonolus.script.printing import PrintColor, PrintFormat
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.layer import LAYER_BPM_LINE, get_z
from sekai.lib.skin import ActiveSkin
from sekai.preview.layout import layout_preview_bar_line, print_at_time


class PreviewSkill(PreviewArchetype):
    name = archetype_names.SKILL

    beat: StandardImport.BEAT = imported()

    time: float = entity_data()

    def preprocess(self):
        self.time = beat_to_time(self.beat)

    def render(self):
        ActiveSkin.skill_line.draw(
            layout_preview_bar_line(self.time, "right"),
            z=get_z(LAYER_BPM_LINE),
            a=0.8,
        )
        print_at_time(
            self.time,
            self.time,
            fmt=PrintFormat.SKILL,
            color=PrintColor.GREEN,
            side="right",
        )


class PreviewFeverChance(PreviewArchetype):
    name = archetype_names.FEVER_CHANCE

    beat: StandardImport.BEAT = imported()

    time: float = entity_data()

    def preprocess(self):
        self.time = beat_to_time(self.beat)

    def render(self):
        ActiveSkin.fever_chance_line.draw(
            layout_preview_bar_line(self.time, "right"),
            z=get_z(LAYER_BPM_LINE),
            a=0.8,
        )
        print_at_time(
            self.time,
            self.time,
            fmt=PrintFormat.FEVER_CHANCE,
            color=PrintColor.CYAN,
            side="right",
        )


class PreviewFeverStart(PreviewArchetype):
    name = archetype_names.FEVER_START

    beat: StandardImport.BEAT = imported()

    time: float = entity_data()

    def preprocess(self):
        self.time = beat_to_time(self.beat)

    def render(self):
        ActiveSkin.fever_start_line.draw(
            layout_preview_bar_line(self.time, "right"),
            z=get_z(LAYER_BPM_LINE),
            a=0.8,
        )
        print_at_time(
            round(self.time, 2),
            self.time,
            fmt=PrintFormat.FEVER_CHANCE,
            color=PrintColor.BLUE,
            side="right",
        )


PREVIEW_EVENT_ARCHETYPES = (PreviewSkill, PreviewFeverChance, PreviewFeverStart)
