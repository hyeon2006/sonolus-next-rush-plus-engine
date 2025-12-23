from sonolus.script.archetype import PlayArchetype, callback, entity_info_at
from sonolus.script.containers import sort_linked_entities
from sonolus.script.globals import level_memory

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
from sekai.lib.ui import init_ui
from sekai.play import input_manager, note, stage
from sekai.play.events import Skill


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


class Initialization(PlayArchetype):
    name = archetype_names.INITIALIZATION

    score_mode: ConcreteScoreMode = imported(name="scoreMode", default=ScoreMode.UNWEIGHTED_COMBO)
    initial_life: int = imported(name="initialLife", default=1000)

    @callback(order=-1)
    def preprocess(self):
        init_level_config(self.score_mode)
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

        for note_archetype in note.NOTE_ARCHETYPES:
            init_note_life(note_archetype)

        sorted_linked_list()

    def initialize(self):
        stage.Stage.spawn()
        input_manager.InputManager.spawn()

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    def update_parallel(self):
        self.despawn = True


def sorted_linked_list():
    entity_count = 0
    while entity_info_at(entity_count).index == entity_count:
        entity_count += 1
    note_head, note_length, skill_head, skill_length = initial_list(entity_count)

    if note_length > 0:
        sorted_note_head = sort_entities(note_head, note.BaseNote)
        setting_count(sorted_note_head.index)

    if skill_length > 0:
        sorted_skill_head = sort_entities(skill_head, Skill)
        count_skill(sorted_skill_head.index)


def initial_list(entity_count):
    note_head = 0
    note_length = 0
    skill_head = 0
    skill_length = 0

    note_id = note.BaseNote._compile_time_id()
    skill_id = Skill._compile_time_id()
    for i in range(entity_count):
        entity_index: int = entity_count - 1 - i
        info = entity_info_at(entity_index)
        mro = PlayArchetype._get_mro_id_array(info.archetype_id)
        is_note = note_id in mro
        is_skill = skill_id in mro
        if (is_note and note.BaseNote.at(entity_index).is_scored) or is_skill:
            if is_note:
                note.BaseNote.at(entity_index).init_data()
                note.BaseNote.at(entity_index).next_ref.index = note_head
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


def setting_count(head: int) -> None:
    ptr = head
    count = 0
    while ptr > 0:
        count += 1
        note.BaseNote.at(ptr).count += count
        if (
            note.FeverChanceEventCounter.fever_chance_time
            <= note.BaseNote.at(ptr).target_time
            < note.FeverChanceEventCounter.fever_start_time
        ):
            note.FeverChanceEventCounter.fever_first_count = (
                min(note.BaseNote.at(ptr).count, note.FeverChanceEventCounter.fever_first_count)
                if note.FeverChanceEventCounter.fever_first_count != 0
                else note.BaseNote.at(ptr).count
            )
            note.FeverChanceEventCounter.fever_last_count = max(
                note.BaseNote.at(ptr).count, note.FeverChanceEventCounter.fever_last_count
            )

        ptr = note.BaseNote.at(ptr).next_ref.index


def count_skill(head: int) -> None:
    ptr = head
    count = 0
    while ptr > 0:
        Skill.at(ptr).count = count
        count += 1
        ptr = Skill.at(ptr).next_ref.index
