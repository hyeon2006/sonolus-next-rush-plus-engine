from sonolus.script.archetype import EntityRef, PlayArchetype, callback, entity_data, imported
from sonolus.script.runtime import time

from sekai.lib import archetype_names
from sekai.lib.sim_line import draw_sim_line
from sekai.lib.timescale import group_hide_notes
from sekai.play.note import BaseNote


class SimLine(PlayArchetype):
    name = archetype_names.SIM_LINE

    left_ref: EntityRef[BaseNote] = imported(name="left")
    right_ref: EntityRef[BaseNote] = imported(name="right")

    spawn_time: float = entity_data()

    @callback(order=1)
    def preprocess(self):
        self.spawn_time = min(self.left.start_time, self.right.start_time)

    def spawn_order(self) -> float:
        return self.spawn_time

    def should_spawn(self) -> bool:
        return time() >= self.spawn_time

    def update_parallel(self):
        if self.left.is_despawned or self.right.is_despawned or time() > self.left.target_time:
            self.despawn = True
            return
        if group_hide_notes(self.left.timescale_group) or group_hide_notes(self.right.timescale_group):
            return
        draw_sim_line(
            left_lane=self.left.lane,
            left_progress=self.left.progress,
            left_target_time=self.left.target_time,
            right_lane=self.right.lane,
            right_progress=self.right.progress,
            right_target_time=self.right.target_time,
        )

    @property
    def left(self) -> BaseNote:
        return self.left_ref.get()

    @property
    def right(self) -> BaseNote:
        return self.right_ref.get()
