from sonolus.script.archetype import WatchArchetype, callback, entity_info_at
from sonolus.script.bucket import Judgment
from sonolus.script.containers import sort_linked_entities
from sonolus.script.runtime import is_replay

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.level_config import init_level_config
from sekai.lib.note import init_life, init_score
from sekai.lib.options import ConcreteScoreMode, ScoreMode
from sekai.lib.particle import init_particles
from sekai.lib.skin import init_skin
from sekai.lib.stage import schedule_lane_sfx
from sekai.lib.streams import Streams
from sekai.lib.ui import init_ui
from sekai.watch.note import WATCH_NOTE_ARCHETYPES, WatchBaseNote
from sekai.watch.stage import WatchScheduledLaneEffect, WatchStage


class WatchInitialization(WatchArchetype):
    name = archetype_names.INITIALIZATION

    score_mode: ConcreteScoreMode = imported(name="scoreMode", default=ScoreMode.UNWEIGHTED_COMBO)
    initial_life: int = imported(name="initialLife", default=1000)

    @callback(order=-1)
    def preprocess(self):
        init_level_config(self.score_mode)
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

        sorted_linked_list()


def sorted_linked_list():
    entity_count = 0
    while entity_info_at(entity_count).index == entity_count:
        entity_count += 1
    list_head, list_length = initial_list(entity_count)

    if list_length == 0:
        return

    sorted_list_head = sort_entities(list_head)
    WatchBaseNote.at(0).sorted_list_head = sorted_list_head

    setting_combo(sorted_list_head.index)


def initial_list(entity_count):
    list_head = 0
    list_length = 0
    for i in range(entity_count):
        entity_index = entity_count - 1 - i
        if WatchBaseNote.at(entity_index).is_scored:
            list_length += 1
            WatchBaseNote.at(entity_index).next_ref.index = list_head
            list_head = entity_index
    return list_head, list_length


def sort_entities(index: int):
    head = WatchBaseNote.at(index)
    return sort_linked_entities(
        head.ref(),
        get_value=lambda head: head.target_time,
        get_next_ref=lambda head: head.next_ref,
    )


def setting_combo(head: int) -> None:
    ptr = head
    combo = 0
    ap = False
    while ptr != 0:
        if (is_replay() and WatchBaseNote.at(ptr).ap) or ap:
            ap = True
            WatchBaseNote.at(ptr).ap = True

        judgment = WatchBaseNote.at(ptr).judgment
        if is_replay() and (judgment == Judgment.GOOD or Judgment.MISS):
            combo = 0
        else:
            combo += 1
        WatchBaseNote.at(ptr).combo = combo
        ptr = WatchBaseNote.at(ptr).next_ref.index
