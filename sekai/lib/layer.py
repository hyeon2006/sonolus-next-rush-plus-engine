from sonolus.script.interval import clamp

LAYER_BACKGROUND_COVER = 0
LAYER_STAGE_COVER = 1
LAYER_STAGE = 2
LAYER_COVER = 3
LAYER_STAGE_LANE = 4
LAYER_JUDGMENT_LINE = 5
LAYER_SLOT_EFFECT = 6

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


"""def get_z(layer: int | float, time: float = 0.0, lane: int | float = 0.0, etc: int | float = 0.0) -> float:
    return (1 / 512) * etc + (1 / 512) * abs(lane) - 5 * time + 512 * layer"""


def get_z(layer: int, time: float = 0.0, lane: float = 0.0, etc: int | float = 0.0, current_time: float = 0.0) -> float:
    # Layer - <6 bits (-1 - 45)
    # Time - 14 bits (-8192 - 8191) / 256
    # Lane - 8 bits (0 - 255) / 16
    # Etc - 3 bits (0 - 7)

    b_0_6 = int(clamp(layer + 1, 0, 45))
    b_6_20 = int(clamp((time - current_time) * 256 + 8192, 0, 16383))
    b_20_28 = int(clamp(abs(lane) * 16, 0, 255))
    b_28_31 = int(clamp(etc, 0, 7))

    b_5_8, b_8_19 = split_bits(b_6_20, 14, 2)
    b_0_8 = concat_bits(b_0_6, b_5_8, 2)
    b_8_27 = concat_bits(b_8_19, b_20_28, 8)
    b_8_31 = concat_bits(b_8_27, b_28_31, 3)

    exponent = b_0_8 - 60
    mantissa = (b_8_31 + 2**23) / (2**23)
    return mantissa * (2**exponent)


def split_bits(value: int, total_bits: int, left_bits: int) -> tuple[int, int]:
    right_bits = total_bits - left_bits
    divisor = 2**right_bits
    left_value = value // divisor
    right_value = value % divisor
    return left_value, right_value


def concat_bits(left_value: int, right_value: int, right_bits: int) -> int:
    return (left_value * (2**right_bits)) + right_value
