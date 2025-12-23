from sonolus.script.archetype import WatchArchetype, callback, entity_info_at, imported
from sonolus.script.bucket import Judgment
from sonolus.script.containers import sort_linked_entities
from sonolus.script.globals import level_memory
from sonolus.script.runtime import is_replay

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layer import (
    LAYER_BACKGROUND_SIDE,
    LAYER_DAMAGE,
    LAYER_GAUGE,
    LAYER_JUDGMENT,
    LAYER_SKILL_BAR,
    LAYER_SKILL_ETC,
    LAYER_STAGE,
    get_z,
)
from sekai.lib.layout import init_layout
from sekai.lib.note import init_note_life, init_score
from sekai.lib.particle import init_particles
from sekai.lib.skin import init_skin
from sekai.lib.stage import schedule_lane_sfx
from sekai.lib.streams import Streams
from sekai.lib.ui import init_ui
from sekai.watch.events import Skill
from sekai.watch.note import WATCH_NOTE_ARCHETYPES, FeverChanceEventCounter, WatchBaseNote
from sekai.watch.stage import WatchScheduledLaneEffect, WatchStage


@level_memory
class LayerCache:
    judgment: float
    judgment1: float
    judgment2: float
    damage: float
    fever_chance_cover: float
    fever_chance_side: float
    fever_chance_gauge: float
    skill_bar: float
    skill_etc: float


class WatchInitialization(WatchArchetype):
    name = archetype_names.INITIALIZATION
    is_multi: bool = imported()

    @callback(order=-1)
    def preprocess(self):
        init_layout()
        init_skin()
        init_particles()
        init_ui()
        init_buckets()
        init_score()

        LayerCache.judgment = get_z(layer=LAYER_JUDGMENT)
        LayerCache.judgment1 = get_z(layer=LAYER_JUDGMENT, etc=1)
        LayerCache.judgment2 = get_z(layer=LAYER_JUDGMENT, etc=2)
        LayerCache.damage = get_z(layer=LAYER_DAMAGE)
        LayerCache.fever_chance_cover = get_z(layer=LAYER_BACKGROUND_SIDE)
        LayerCache.fever_chance_side = get_z(layer=LAYER_STAGE)
        LayerCache.fever_chance_gauge = get_z(layer=LAYER_GAUGE)
        LayerCache.skill_bar = get_z(layer=LAYER_SKILL_BAR)
        LayerCache.skill_etc = get_z(layer=LAYER_SKILL_ETC)

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
    note_head, note_length, skill_head, skill_length = initial_list(entity_count)

    if note_length > 0:
        sorted_note_head = sort_entities(note_head, WatchBaseNote)
        setting_combo(sorted_note_head.index)

    if skill_length > 0:
        sorted_skill_head = sort_entities(skill_head, Skill)
        count_skill(sorted_skill_head.index)


def initial_list(entity_count):
    note_head = 0
    note_length = 0
    skill_head = 0
    skill_length = 0

    note_id = WatchBaseNote._compile_time_id()
    skill_id = Skill._compile_time_id()
    for i in range(entity_count):
        entity_index = entity_count - 1 - i
        info = entity_info_at(entity_index)
        mro = WatchArchetype._get_mro_id_array(info.archetype_id)
        is_note = note_id in mro
        is_skill = skill_id in mro
        if (is_note and WatchBaseNote.at(entity_index).is_scored) or is_skill:
            if is_note:
                WatchBaseNote.at(entity_index).init_data()
                WatchBaseNote.at(entity_index).next_ref.index = note_head
                note_head = entity_index
                note_length += 1
            elif is_skill:
                Skill.at(entity_index).next_ref.index = skill_head
                skill_head = entity_index
                skill_length += 1

    return note_head, note_length, skill_head, skill_length


def sort_entities(index: int, entity_cls):
    head = entity_cls.at(index)
    return sort_linked_entities(
        head.ref(),
        get_value=lambda head: head.calc_time,
        get_next_ref=lambda head: head.next_ref,
    )


def setting_combo(head: int) -> None:
    ptr = head
    combo = 0
    count = 0
    ap = False
    accuracy = head
    damage_flash = head
    while ptr > 0:
        judgment = WatchBaseNote.at(ptr).judgment
        if is_replay() and judgment in (Judgment.GOOD, Judgment.MISS):
            combo = 0
            if (
                FeverChanceEventCounter.fever_chance_time
                <= WatchBaseNote.at(ptr).calc_time
                < FeverChanceEventCounter.fever_start_time
            ):
                FeverChanceEventCounter.fever_chance_cant_super_fever = True
        else:
            combo += 1
        WatchBaseNote.at(ptr).combo = combo

        if is_replay() and judgment != Judgment.PERFECT:
            ap = True
        if is_replay() and ap:
            WatchBaseNote.at(ptr).at(ptr).ap = True

        if is_replay() and judgment != Judgment.PERFECT and WatchBaseNote.at(ptr).at(ptr).played_hit_effects:
            WatchBaseNote.at(ptr).at(accuracy).next_ref_accuracy.index = ptr
            accuracy = ptr

        if is_replay() and judgment == Judgment.MISS:
            WatchBaseNote.at(ptr).at(damage_flash).next_ref_damage_flash.index = ptr
            damage_flash = ptr

        count += 1
        WatchBaseNote.at(ptr).count = count
        if (
            FeverChanceEventCounter.fever_chance_time
            <= WatchBaseNote.at(ptr).calc_time
            < FeverChanceEventCounter.fever_start_time
        ):
            FeverChanceEventCounter.fever_first_count = (
                min(WatchBaseNote.at(ptr).count, FeverChanceEventCounter.fever_first_count)
                if FeverChanceEventCounter.fever_first_count != 0
                else WatchBaseNote.at(ptr).count
            )
            FeverChanceEventCounter.fever_last_count = max(
                WatchBaseNote.at(ptr).count, FeverChanceEventCounter.fever_last_count
            )
        ptr = WatchBaseNote.at(ptr).next_ref.index


def count_skill(head: int) -> None:
    ptr = head
    count = 0
    while ptr > 0:
        Skill.at(ptr).count = count
        count += 1
        ptr = Skill.at(ptr).next_ref.index
