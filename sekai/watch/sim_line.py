from sonolus.script.archetype import EntityRef, WatchArchetype, callback, entity_data, imported
from sonolus.script.runtime import is_replay

from sekai.lib import archetype_names
from sekai.lib.sim_line import draw_sim_line
from sekai.lib.timescale import group_hide_notes
from sekai.watch.note import WatchBaseNote


class WatchSimLine(WatchArchetype):
    name = archetype_names.SIM_LINE

    left_ref: EntityRef[WatchBaseNote] = imported(name="left")
    right_ref: EntityRef[WatchBaseNote] = imported(name="right")

    start_time: float = entity_data()
    end_time: float = entity_data()

    @callback(order=1)
    def preprocess(self):
        self.start_time = min(self.left.start_time, self.right.start_time)
        if is_replay():
            self.end_time = min(self.left.end_time, self.right.end_time, self.left.target_time)
        else:
            self.end_time = min(self.left.target_time, self.right.target_time)

    def spawn_time(self) -> float:
        return self.start_time

    def despawn_time(self) -> float:
        return self.end_time

    def update_parallel(self):
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
    def left(self) -> WatchBaseNote:
        return self.left_ref.get()

    @property
    def right(self) -> WatchBaseNote:
        return self.right_ref.get()
