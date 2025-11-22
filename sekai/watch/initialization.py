from sonolus.script.archetype import WatchArchetype, callback

from sekai.lib import archetype_names
from sekai.lib.buckets import init_buckets
from sekai.lib.layout import init_layout
from sekai.lib.note import init_note_life, init_score
from sekai.lib.skin import init_skin
from sekai.lib.stage import schedule_lane_sfx
from sekai.lib.streams import Streams
from sekai.lib.ui import init_ui
from sekai.watch.note import WATCH_NOTE_ARCHETYPES
from sekai.watch.stage import WatchScheduledLaneEffect, WatchStage


class WatchInitialization(WatchArchetype):
    name = archetype_names.INITIALIZATION

    @callback(order=-1)
    def preprocess(self):
        init_layout()
        init_ui()
        init_skin()
        init_buckets()
        init_score()

        for note_archetype in WATCH_NOTE_ARCHETYPES:
            init_note_life(note_archetype)

        WatchStage.spawn()

        for input_time, lanes in Streams.empty_input_lanes.iter_items_from(-2):
            for lane in lanes:
                schedule_lane_sfx(lane, input_time)
                WatchScheduledLaneEffect.spawn(lane=lane, target_time=input_time)
