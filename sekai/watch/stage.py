from sonolus.script.archetype import WatchArchetype, entity_memory
from sonolus.script.runtime import is_skip

from sekai.lib import archetype_names
from sekai.lib.layer import (
    LAYER_BACKGROUND_COVER,
    LAYER_COVER,
    LAYER_COVER_LINE,
    LAYER_JUDGMENT,
    LAYER_JUDGMENT_LINE,
    LAYER_STAGE,
    LAYER_STAGE_COVER,
    LAYER_STAGE_LANE,
    get_z,
)
from sekai.lib.stage import draw_stage_and_accessories, play_lane_particle


class WatchStage(WatchArchetype):
    name = archetype_names.STAGE
    z_layer_stage_lane: float = entity_memory()
    z_layer_judgment: float = entity_memory()
    z_layer_cover: float = entity_memory()
    z_layer_cover_line: float = entity_memory()
    z_layer_judgment_line: float = entity_memory()
    z_layer_background_cover: float = entity_memory()
    z_layer_stage: float = entity_memory()
    z_layer_stage_cover: float = entity_memory()

    def spawn_time(self) -> float:
        return -1e8

    def despawn_time(self) -> float:
        return 1e8

    def initialize(self):
        self.z_layer_stage_lane = get_z(LAYER_STAGE_LANE)
        self.z_layer_cover = get_z(LAYER_COVER)
        self.z_layer_cover_line = get_z(LAYER_COVER_LINE)
        self.z_layer_judgment = get_z(LAYER_JUDGMENT)
        self.z_layer_judgment_line = get_z(LAYER_JUDGMENT_LINE)
        self.z_layer_background_cover = get_z(LAYER_BACKGROUND_COVER)
        self.z_layer_stage = get_z(LAYER_STAGE)
        self.z_layer_stage_cover = get_z(LAYER_STAGE_COVER)

    def update_parallel(self):
        draw_stage_and_accessories(
            self.z_layer_stage_lane,
            self.z_layer_stage_cover,
            self.z_layer_stage,
            self.z_layer_judgment_line,
            self.z_layer_cover,
            self.z_layer_cover_line,
            self.z_layer_judgment,
            self.z_layer_background_cover,
        )


class WatchScheduledLaneEffect(WatchArchetype):
    name = archetype_names.SCHEDULED_LANE_EFFECT

    lane: float = entity_memory()
    target_time: float = entity_memory()

    def spawn_time(self) -> float:
        return self.target_time

    def despawn_time(self) -> float:
        return self.target_time + 1

    def initialize(self):
        if is_skip():
            return
        play_lane_particle(self.lane)
