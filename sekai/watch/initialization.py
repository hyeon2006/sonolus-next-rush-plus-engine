from sonolus.script.archetype import WatchArchetype, callback, entity_info_at
from sonolus.script.bucket import Judgment
from sonolus.script.containers import sort_linked_entities
from sonolus.script.runtime import is_replay

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.note import init_note_life, init_score
from sekai.lib.options import Options
from sekai.lib.particle import init_particles
from sekai.lib.skin import combo_label, combo_number, damage_flash, init_skin, judgment_text
from sekai.lib.stage import schedule_lane_sfx
from sekai.lib.streams import Streams
from sekai.lib.ui import init_ui
from sekai.watch.note import WATCH_NOTE_ARCHETYPES, WatchBaseNote
from sekai.watch.stage import WatchScheduledLaneEffect, WatchStage


class WatchInitialization(WatchArchetype):
    name = archetype_names.INITIALIZATION

    @callback(order=-1)
    def preprocess(self):
        init_layout()
        init_ui()
        init_skin()
        init_particles()
        init_buckets()
        init_score()

        for note_archetype in WATCH_NOTE_ARCHETYPES:
            init_note_life(note_archetype)

        WatchStage.spawn()

        for input_time, lanes in Streams.empty_input_lanes.iter_items_from(-2):
            for lane in lanes:
                schedule_lane_sfx(lane, input_time)
                WatchScheduledLaneEffect.spawn(lane=lane, target_time=input_time)

        if (
            not Options.hide_custom
            or (Options.custom_combo and combo_label.custom_available)
            or (Options.custom_combo and combo_number.custom_available)
            or (Options.custom_judgment and judgment_text.custom_available)
            or (Options.custom_accuracy and Options.custom_accuracy and is_replay())
            or (Options.custom_damage and damage_flash.custom_available and is_replay())
        ):
            sorted_linked_list()


def sorted_linked_list():
    entity_count = 0
    while entity_info_at(entity_count).index == entity_count:
        entity_count += 1
    list_head, list_length = initial_list(entity_count)

    if list_length == 0:
        return

    sorted_list_head = sort_entities(list_head)

    setting_combo(sorted_list_head.index)


def initial_list(entity_count):
    list_head = 0
    list_length = 0
    watch_note_id = WatchBaseNote._compile_time_id()
    for i in range(entity_count):
        entity_index = entity_count - 1 - i
        info = entity_info_at(entity_index)
        is_watch_note = watch_note_id in WatchBaseNote._get_mro_id_array(info.archetype_id)
        if is_watch_note and WatchBaseNote.at(entity_index).is_scored:
            WatchBaseNote.at(entity_index).init_data()
            list_length += 1
            WatchBaseNote.at(entity_index).next_ref.index = list_head
            list_head = entity_index
    return list_head, list_length


def sort_entities(index: int):
    head = WatchBaseNote.at(index)
    return sort_linked_entities(
        head.ref(),
        get_value=lambda head: head.hit_time,
        get_next_ref=lambda head: head.next_ref,
    )


def setting_combo(head: int) -> None:
    ptr = head
    combo = 0
    ap = False
    accuracy = head
    damage_flash = head
    while ptr > 0:
        judgment = WatchBaseNote.at(ptr).judgment
        if is_replay() and judgment in (Judgment.GOOD, Judgment.MISS):
            combo = 0
        else:
            combo += 1
        WatchBaseNote.at(ptr).combo = combo

        if is_replay() and judgment != Judgment.PERFECT:
            ap = True
        if is_replay() and ap:
            WatchBaseNote.at(ptr).ap = True

        if is_replay() and judgment != Judgment.PERFECT and WatchBaseNote.at(ptr).played_hit_effects:
            WatchBaseNote.at(accuracy).next_ref_accuracy.index = ptr
            accuracy = ptr

        if is_replay() and judgment == Judgment.MISS:
            WatchBaseNote.at(damage_flash).next_ref_damage_flash.index = ptr
            damage_flash = ptr
        ptr = WatchBaseNote.at(ptr).next_ref.index
