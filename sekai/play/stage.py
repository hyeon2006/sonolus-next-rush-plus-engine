from sonolus.script.archetype import PlayArchetype, callback, entity_memory
from sonolus.script.array import Dim
from sonolus.script.containers import VarArray
from sonolus.script.interval import clamp
from sonolus.script.quad import Rect
from sonolus.script.runtime import offset_adjusted_time, touches

from sekai.lib import archetype_names
from sekai.lib.custom_elements import draw_score_number
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
from sekai.lib.layout import layout_hitbox
from sekai.lib.stage import draw_stage_and_accessories, play_lane_hit_effects
from sekai.lib.streams import Streams
from sekai.play import custom_elements, input_manager


class Stage(PlayArchetype):
    name = archetype_names.STAGE
    z_layer_stage_lane: float = entity_memory()
    z_layer_judgment: float = entity_memory()
    z_layer_cover: float = entity_memory()
    z_layer_cover_line: float = entity_memory()
    z_layer_judgment_line: float = entity_memory()
    z_layer_background_cover: float = entity_memory()
    z_layer_stage: float = entity_memory()
    z_layer_stage_cover: float = entity_memory()
    z_layer_score: float = entity_memory()
    z_layer_score_glow: float = entity_memory()
    total_hitbox: Rect = entity_memory()
    w_scale: float = entity_memory()

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    def initialize(self):
        self.z_layer_stage_lane = get_z(LAYER_STAGE_LANE)
        self.z_layer_cover = get_z(LAYER_COVER)
        self.z_layer_cover_line = get_z(LAYER_COVER_LINE)
        self.z_layer_judgment = get_z(LAYER_JUDGMENT)
        self.z_layer_judgment_line = get_z(LAYER_JUDGMENT_LINE)
        self.z_layer_background_cover = get_z(LAYER_BACKGROUND_COVER)
        self.z_layer_stage = get_z(LAYER_STAGE)
        self.z_layer_stage_cover = get_z(LAYER_STAGE_COVER)
        self.z_layer_score = get_z(layer=LAYER_JUDGMENT)
        self.z_layer_score_glow = get_z(layer=LAYER_JUDGMENT, etc=1)
        self.total_hitbox = layout_hitbox(-7, 7)
        self.w_scale = (self.total_hitbox.r - self.total_hitbox.l) / 14

    @callback(order=2)
    def touch(self):
        empty_lanes = VarArray[float, Dim[16]].new()
        for touch in touches():
            if not self.total_hitbox.contains_point(touch.position):
                continue
            if not input_manager.is_allowed_empty(touch):
                continue
            lane = (touch.position.x - self.total_hitbox.l) / self.w_scale - 7
            rounded_lane = clamp(round(lane - 0.5) + 0.5, -5.5, 5.5)
            if touch.started:
                play_lane_hit_effects(rounded_lane)
                if not empty_lanes.is_full():
                    empty_lanes.append(rounded_lane)
            else:
                prev_lane = (touch.prev_position.x - self.total_hitbox.l) / self.w_scale - 7
                prev_rounded_lane = clamp(round(prev_lane - 0.5) + 0.5, -5.5, 5.5)
                if rounded_lane != prev_rounded_lane:
                    play_lane_hit_effects(rounded_lane)
                    if not empty_lanes.is_full():
                        empty_lanes.append(rounded_lane)
        if len(empty_lanes) > 0:
            Streams.empty_input_lanes[offset_adjusted_time()] = empty_lanes

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
        draw_score_number(
            ap=custom_elements.ComboJudgeMemory.ap,
            score=round(custom_elements.ScoreIndicator.score, 4),
            z1=self.z_layer_score,
            z2=self.z_layer_score_glow,
        )
