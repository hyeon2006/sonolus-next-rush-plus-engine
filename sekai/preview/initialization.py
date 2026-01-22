from sonolus.script.archetype import PreviewArchetype, callback, entity_info_at, imported
from sonolus.script.containers import sort_linked_entities
from sonolus.script.printing import PrintColor, PrintFormat
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.layer import LAYER_BEAT_LINE, get_z
from sekai.lib.level_config import EngineRevision, init_level_config
from sekai.lib.particle import init_particles
from sekai.lib.skin import ActiveSkin, init_skin
from sekai.lib.ui import init_ui
from sekai.preview.events import PreviewSkill
from sekai.preview.layout import (
    PREVIEW_COLUMN_SECS,
    PreviewData,
    PreviewLayout,
    init_preview_layout,
    layout_preview_bar_line,
    print_at_col_top,
)
from sekai.preview.stage import draw_preview_cover, draw_preview_stage


class PreviewInitialization(PreviewArchetype):
    name = archetype_names.INITIALIZATION

    revision: EngineRevision = imported(name="revision", default=EngineRevision.LATEST)

    @callback(order=1)
    def preprocess(self):
        init_level_config(self.revision)
        init_ui()
        init_skin()
        init_particles()
        init_preview_layout()
        init_skill()

    def render(self):
        draw_preview_stage()
        draw_preview_cover()
        print_preview_col_head_text()
        draw_beat_lines()


def print_preview_col_head_text():
    combo = 0
    for col in range(PreviewLayout.column_count):
        if col < len(PreviewData.note_counts_by_col):
            combo += PreviewData.note_counts_by_col[col]
            print_at_col_top(combo, col, fmt=PrintFormat.ENTITY_COUNT, color=PrintColor.RED, side="right")
        print_at_col_top(col * PREVIEW_COLUMN_SECS, col, fmt=PrintFormat.TIME, color=PrintColor.CYAN, side="left")


def draw_beat_lines():
    for beat in range(int(PreviewData.max_beat) + 1):
        for beat_offset, extend_scale in (
            (0, 0.3),
            (0.25, 0.1),
            (0.5, 0.2),
            (0.75, 0.1),
        ):
            layout = layout_preview_bar_line(
                beat_to_time(beat + beat_offset), extend="left_only", extend_scale=extend_scale
            )
            ActiveSkin.beat_line.draw(layout, z=get_z(LAYER_BEAT_LINE), a=0.5)
            layout = layout_preview_bar_line(
                beat_to_time(beat + beat_offset), extend="right_only", extend_scale=extend_scale
            )
            ActiveSkin.beat_line.draw(layout, z=get_z(LAYER_BEAT_LINE), a=0.5)


def init_skill():
    entity_count = 0
    while entity_info_at(entity_count).index == entity_count:
        entity_count += 1
    list_head, list_length = initial_list(entity_count)

    if list_length == 0:
        return

    sorted_list_head = sort_entities(list_head)

    setting_count(sorted_list_head.index)


def initial_list(entity_count):
    list_head = 0
    list_length = 0
    watch_note_id = PreviewSkill._compile_time_id()
    for i in range(entity_count):
        entity_index: int = entity_count - 1 - i
        info = entity_info_at(entity_index)
        is_watch_note = watch_note_id in PreviewSkill._get_mro_id_array(info.archetype_id)
        if is_watch_note:
            PreviewSkill.at(entity_index).preprocess()
            list_length += 1
            PreviewSkill.at(entity_index).next_ref.index = list_head
            list_head = entity_index
    return list_head, list_length


def sort_entities(index: int):
    head = PreviewSkill.at(index)
    return sort_linked_entities(
        head.ref(),
        get_value=lambda head: head.time,
        get_next_ref=lambda head: head.next_ref,
    )


def setting_count(head: int) -> None:
    ptr = head
    count = 0
    while ptr > 0:
        count += 1
        PreviewSkill.at(ptr).num += count

        ptr = PreviewSkill.at(ptr).next_ref.index
