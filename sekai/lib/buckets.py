from typing import Literal, assert_never

from sonolus.script.bucket import Bucket, JudgmentWindow, bucket, bucket_sprite, buckets
from sonolus.script.interval import Interval
from sonolus.script.sprite import Sprite
from sonolus.script.text import StandardText

from sekai.lib.skin import Skin

WINDOW_SCALE = 1000  # Windows are in ms


def create_bucket_sprites(
    body: Sprite | None = None,
    body_fallback: Sprite | None = None,
    arrow: Sprite | None = None,
    tick: Sprite | None = None,
    connector: Sprite | None = None,
    body_pos: Literal["left", "middle", "right"] = "middle",
):
    sprites = []

    if body_pos == "left":
        connector_x = 0.5
        body_x = -2.0
    elif body_pos == "middle":
        connector_x = 0.0
        body_x = 0.0
    elif body_pos == "right":
        connector_x = -0.5
        body_x = 2.0
    else:
        assert_never(body_pos)

    if connector is not None:
        sprites.append(
            bucket_sprite(
                sprite=connector,
                x=connector_x,
                y=0,
                w=2,
                h=5,
                rotation=-90,
            )
        )

    if body is not None:
        sprite_args = {
            "sprite": body,
            "x": body_x,
            "y": 0,
            "w": 2,
            "h": 2,
            "rotation": -90,
        }
        if body_fallback is not None:
            sprite_args["fallback_sprite"] = body_fallback
        sprites.append(bucket_sprite(**sprite_args))

    if arrow is not None:
        sprites.append(
            bucket_sprite(
                sprite=arrow,
                x=body_x + 1,
                y=0,
                w=2,
                h=2,
                rotation=-90,
            )
        )

    if tick is not None:
        sprites.append(
            bucket_sprite(
                sprite=tick,
                x=body_x,
                y=0,
                w=2,
                h=2,
                rotation=-90,
            )
        )

    return sprites


@buckets
class Buckets:
    # Normal buckets
    normal_tap: Bucket = bucket(
        sprites=create_bucket_sprites(body=Skin.normal_note_fallback),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_tap: Bucket = bucket(
        sprites=create_bucket_sprites(body=Skin.critical_note_fallback),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.flick_note_fallback,
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.critical_note_fallback,
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.normal_trace_note_left,
            body_fallback=Skin.normal_trace_note_fallback,
            tick=Skin.normal_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            tick=Skin.critical_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.trace_flick_note_left,
            body_fallback=Skin.trace_flick_tick_note_fallback,
            tick=Skin.trace_flick_tick_note,
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            tick=Skin.critical_trace_tick_note,
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    # Head buckets
    normal_head_tap: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.slide_note_fallback,
            body_pos="left",
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_head_tap: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_note_fallback,
            body_pos="left",
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_head_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.flick_note_fallback,
            body_pos="left",
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_head_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_note_fallback,
            body_pos="left",
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_head_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.normal_trace_note_left,
            body_fallback=Skin.normal_trace_note_fallback,
            body_pos="left",
            tick=Skin.normal_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_head_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            body_pos="left",
            tick=Skin.critical_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_head_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.trace_flick_note_left,
            body_fallback=Skin.trace_flick_tick_note_fallback,
            body_pos="left",
            tick=Skin.trace_flick_tick_note,
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_head_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            body_pos="left",
            tick=Skin.critical_trace_tick_note,
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    # Tail buckets
    normal_tail_release: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.slide_note_end_fallback,
            body_pos="right",
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_tail_release: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_note_end_fallback,
            body_pos="right",
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_tail_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.flick_note_fallback,
            body_pos="right",
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_tail_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_note_end_fallback,
            body_pos="right",
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_tail_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.normal_trace_note_left,
            body_fallback=Skin.normal_trace_note_fallback,
            body_pos="right",
            tick=Skin.normal_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_tail_trace: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            body_pos="right",
            tick=Skin.critical_trace_tick_note,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )

    normal_tail_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.normal_slide_connector_active,
            body=Skin.trace_flick_note_left,
            body_fallback=Skin.trace_flick_tick_note_fallback,
            body_pos="right",
            tick=Skin.trace_flick_tick_note,
            arrow=Skin.flick_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )
    critical_tail_trace_flick: Bucket = bucket(
        sprites=create_bucket_sprites(
            connector=Skin.critical_slide_connector_active,
            body=Skin.critical_trace_note_left,
            body_fallback=Skin.critical_trace_note_fallback,
            body_pos="right",
            tick=Skin.critical_trace_tick_note,
            arrow=Skin.critical_arrow_fallback,
        ),
        unit=StandardText.MILLISECOND_UNIT,
    )


def init_buckets():
    Buckets.normal_tap.window @= TAP_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_tap.window @= TAP_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_flick.window @= FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_flick.window @= FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_trace.window @= TRACE_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_trace.window @= TRACE_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_trace_flick.window @= TRACE_FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_trace_flick.window @= TRACE_FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_head_tap.window @= TAP_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_head_tap.window @= TAP_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_head_flick.window @= FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_head_flick.window @= FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_head_trace.window @= TRACE_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_head_trace.window @= TRACE_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_head_trace_flick.window @= TRACE_FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_head_trace_flick.window @= TRACE_FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_tail_flick.window @= SLIDE_END_FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_tail_flick.window @= SLIDE_END_FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_tail_trace.window @= SLIDE_END_TRACE_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_tail_trace.window @= SLIDE_END_TRACE_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_tail_trace_flick.window @= TRACE_FLICK_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_tail_trace_flick.window @= TRACE_FLICK_CRITICAL_WINDOW * WINDOW_SCALE
    Buckets.normal_tail_release.window @= SLIDE_END_NORMAL_WINDOW * WINDOW_SCALE
    Buckets.critical_tail_release.window @= SLIDE_END_CRITICAL_WINDOW * WINDOW_SCALE


def frames_to_window(
    perfect: float | tuple[float, float],
    great: float | tuple[float, float],
    good: float | tuple[float, float],
) -> JudgmentWindow:
    perfect = perfect if isinstance(perfect, tuple) else (perfect, perfect)
    great = great if isinstance(great, tuple) else (great, great)
    good = good if isinstance(good, tuple) else (good, good)
    return JudgmentWindow(
        perfect=Interval(-perfect[0] / 60, perfect[1] / 60),
        great=Interval(-great[0] / 60, great[1] / 60),
        good=Interval(-good[0] / 60, good[1] / 60),
    )


TAP_NORMAL_WINDOW = frames_to_window(2.5, 5, 6.5)
TAP_CRITICAL_WINDOW = frames_to_window(3.3, 4.5, 6.5)

FLICK_NORMAL_WINDOW = frames_to_window(2.5, (6.5, 7.5), (7, 8))
FLICK_CRITICAL_WINDOW = frames_to_window(3.5, (6.5, 7.5), (7, 8.5))

TRACE_NORMAL_WINDOW = frames_to_window(5.0, 5.0, 5.0)
TRACE_CRITICAL_WINDOW = frames_to_window(5.0, 5.0, 5.0)

TRACE_FLICK_NORMAL_WINDOW = frames_to_window((6.5, 7.5), (6.5, 7.5), (6.5, 7.5))
TRACE_FLICK_CRITICAL_WINDOW = frames_to_window((6.5, 7.5), (6.5, 7.5), (6.5, 7.5))

SLIDE_END_NORMAL_WINDOW = frames_to_window((3.5, 4), (6.5, 8), (7.5, 8.5))
SLIDE_END_CRITICAL_WINDOW = frames_to_window((3.5, 4), (6.5, 8), (7.5, 8.5))

SLIDE_END_TRACE_NORMAL_WINDOW = frames_to_window((6.5, 8.0), (6.5, 8.8), (6.5, 8.0))
SLIDE_END_TRACE_CRITICAL_WINDOW = frames_to_window((6.5, 8.0), (6.5, 8.8), (6.5, 8.0))

SLIDE_END_FLICK_NORMAL_WINDOW = frames_to_window((3.5, 4), (6.5, 8), (7.5, 8.5))
SLIDE_END_FLICK_CRITICAL_WINDOW = frames_to_window((3.5, 4), (6.5, 8), (7.5, 8.5))

EMPTY_JUDGMENT_WINDOW = frames_to_window(0, 0, 0)

SLIDE_END_LOCKOUT_DURATION = 0.25

TAP_NORMAL_WINDOW_BAD = Interval(-7.5 / 60, 7.5 / 60)
TAP_CRITICAL_WINDOW_BAD = Interval(-7.5 / 60, 7.5 / 60)

FLICK_NORMAL_WINDOW_BAD = Interval(-7.5 / 60, 8.5 / 60)
FLICK_CRITICAL_WINDOW_BAD = Interval(-7.5 / 60, 8.5 / 60)

def get_judgment_interval(bad_window: Interval, good_window: Interval) -> Interval:
    result = +Interval
    if bad_window != Interval(0, 0):
        result @= bad_window
    else:
        result @= good_window
    return result