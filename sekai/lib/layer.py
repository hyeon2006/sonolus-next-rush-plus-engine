from sonolus.script import runtime
from sonolus.script.numtools import make_comparable_float, quantize_to_step

LAYER_BACKGROUND_COVER = 0
LAYER_STAGE_COVER = 1
LAYER_STAGE = 2
LAYER_COVER = 3
LAYER_COVER_LINE = 4
LAYER_STAGE_LANE = 5
LAYER_JUDGMENT_LINE = 6
LAYER_SLOT_EFFECT = 7

LAYER_BEAT_LINE = 10
LAYER_ACTIVE_SIDE_CONNECTOR_BOTTOM = 11
LAYER_GUIDE_CONNECTOR_BOTTOM = 12
LAYER_ACTIVE_SIDE_CONNECTOR_TOP = 13
LAYER_GUIDE_CONNECTOR_TOP = 14
LAYER_PREVIEW_COVER = 15
LAYER_SIM_LINE = 16
LAYER_TIME_LINE = 17
LAYER_BPM_LINE = 18
LAYER_TIMESCALE_LINE = 19

LAYER_NOTE_SLIM_BODY = 20
LAYER_NOTE_FLICK_BODY = 21
LAYER_NOTE_BODY = 22
LAYER_NOTE_TICK = 23
LAYER_NOTE_ARROW = 24
LAYER_SLOT_GLOW_EFFECT = 25

LAYER_DAMAGE = 31
LAYER_JUDGMENT = 32


def get_z(layer: int, time: float = 0.0, lane: float = 0.0, etc: int = 0) -> float:
    return make_comparable_float(
        quantize_to_step(layer, start=-1, stop=63, step=1),
        quantize_to_step(runtime.time() - time, start=-30, stop=30, step=1 / 256),
        quantize_to_step(abs(lane), start=0, stop=17, step=1 / 16),
        quantize_to_step(etc, start=0, stop=8, step=1),
    )
