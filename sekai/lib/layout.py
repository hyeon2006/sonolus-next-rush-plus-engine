from enum import IntEnum
from math import atan, ceil, floor, log, pi
from typing import assert_never

from sonolus.script.debug import static_error
from sonolus.script.globals import level_data
from sonolus.script.interval import clamp, lerp, remap, unlerp
from sonolus.script.num import Num
from sonolus.script.quad import Quad, QuadLike, Rect
from sonolus.script.runtime import aspect_ratio, screen
from sonolus.script.values import swap
from sonolus.script.vec import Vec2

from sekai.lib.options import Options
from sekai.lib.timescale import CompositeTime

LANE_T = 47 / 850
LANE_B = 1176 / 850

LANE_HITBOX_L = -6
LANE_HITBOX_R = 6
LANE_HITBOX_T = (803 / 850) * 0.6
LANE_HITBOX_B = 1.5

NOTE_H = 75 / 850 / 2
NOTE_EDGE_W = 0.25
NOTE_SLIM_EDGE_W = 0.125

TARGET_ASPECT_RATIO = 16 / 9

# Value between 0 and 1 where smaller values mean a 'harsher' approach with more acceleration.
APPROACH_SCALE = 1.06**-45

# Value above 1 where we cut off drawing sprites. Doesn't really matter as long as it's high enough,
# such that something like a flick arrow below the judge line isn't obviously suddenly cut off.
DEFAULT_APPROACH_CUTOFF = 2.5
DEFAULT_PROGRESS_CUTOFF = 1 - log(DEFAULT_APPROACH_CUTOFF, APPROACH_SCALE)


class FlickDirection(IntEnum):
    UP_OMNI = 0
    UP_LEFT = 1
    UP_RIGHT = 2
    DOWN_OMNI = 3
    DOWN_LEFT = 4
    DOWN_RIGHT = 5


@level_data
class Layout:
    t: float
    field_w: float
    field_h: float
    w_scale: float
    h_scale: float
    scaled_note_h: float
    progress_start: float
    progress_cutoff: float
    flick_speed_threshold: float


def init_layout():
    if Options.lock_stage_aspect_ratio:
        if aspect_ratio() > TARGET_ASPECT_RATIO:
            field_w = screen().h * TARGET_ASPECT_RATIO
            field_h = screen().h
        else:
            field_w = screen().w
            field_h = screen().w / TARGET_ASPECT_RATIO
    else:
        field_w = screen().w
        field_h = screen().h

    Layout.field_w = field_w
    Layout.field_h = field_h

    t = field_h * (0.5 + 1.15875 * (47 / 1176))
    b = field_h * (0.5 - 1.15875 * (803 / 1176))
    w = field_w * ((1.15875 * (1420 / 1176)) / TARGET_ASPECT_RATIO / 12)

    Layout.t = t
    Layout.w_scale = w
    Layout.h_scale = b - t
    Layout.scaled_note_h = NOTE_H * Layout.h_scale

    if Options.stage_cover:
        Layout.progress_start = inverse_approach(lerp(approach(0), 1.0, Options.stage_cover))
    else:
        Layout.progress_start = 0.0

    if Options.hidden:
        Layout.progress_cutoff = inverse_approach(lerp(1.0, approach(0), Options.hidden))
    else:
        Layout.progress_cutoff = DEFAULT_PROGRESS_CUTOFF

    Layout.flick_speed_threshold = 2 * Layout.w_scale


def approach(progress: float) -> float:
    if Options.alternative_approach_curve:
        d_0 = 1 / APPROACH_SCALE
        d_1 = 2.5
        v_1 = (d_0 - d_1) / d_1**2
        d = 1 / lerp(d_0, d_1, progress) if progress < 1 else 1 / d_1 + v_1 * (progress - 1)
        return remap(1 / d_0, 1 / d_1, APPROACH_SCALE, 1, d)
    return APPROACH_SCALE ** (1 - progress)


def inverse_approach(approach_value: float) -> float:
    if Options.alternative_approach_curve:
        d_0 = 1 / APPROACH_SCALE
        d_1 = 2.5
        v_1 = (d_0 - d_1) / d_1**2
        d = remap(APPROACH_SCALE, 1, 1 / d_0, 1 / d_1, approach_value)
        if d <= 1 / d_1:
            return (1 / d - d_0) / (d_1 - d_0)
        else:
            return 1 + (d - 1 / d_1) / v_1
    else:
        return 1 - log(approach_value) / log(APPROACH_SCALE)


def progress_to(to_time: float | CompositeTime, now: float | CompositeTime) -> float:
    match (to_time, now):
        case (CompositeTime(), CompositeTime()):
            return ((now.base - to_time.base) + now.delta - to_time.delta + preempt_time()) / preempt_time()
        case (Num(), Num()):
            return unlerp(to_time - preempt_time(), to_time, now)
        case _:
            static_error("Unexpected types for progress_to")


def preempt_time() -> float:
    return lerp(0.35, 4, unlerp(12, 1, Options.note_speed) ** 1.31)


def get_alpha(target_time: float, now: float | None = None) -> float:
    return 1.0


def transform_vec(v: Vec2) -> Vec2:
    return Vec2(
        v.x * Layout.w_scale,
        v.y * Layout.h_scale + Layout.t,
    )


def transform_quad(q: QuadLike) -> Quad:
    return Quad(
        bl=transform_vec(q.bl),
        br=transform_vec(q.br),
        tl=transform_vec(q.tl),
        tr=transform_vec(q.tr),
    )


def transformed_vec_at(lane: float, travel: float = 1.0) -> Vec2:
    return transform_vec(Vec2(lane * travel, travel))


def touch_x_to_lane(x: float) -> float:
    return x / Layout.w_scale


def perspective_vec(x: float, y: float, travel: float = 1.0) -> Vec2:
    return transform_vec(Vec2(x * y * travel, y * travel))


def perspective_rect(l: float, r: float, t: float, b: float, travel: float = 1.0) -> Quad:
    return transform_quad(
        Quad(
            bl=Vec2(l * b * travel, b * travel),
            br=Vec2(r * b * travel, b * travel),
            tl=Vec2(l * t * travel, t * travel),
            tr=Vec2(r * t * travel, t * travel),
        )
    )


def layout_sekai_stage() -> Quad:
    w = (2048 / 1420) * 12 / 2
    h = 1176 / 850
    rect = Rect(l=-w, r=w, t=LANE_T, b=LANE_T + h)
    return transform_quad(rect)


def layout_lane_by_edges(l: float, r: float) -> Quad:
    return perspective_rect(l=l, r=r, t=LANE_T, b=LANE_B)


def layout_lane(lane: float, size: float) -> Quad:
    return layout_lane_by_edges(lane - size, lane + size)


def layout_stage_cover() -> Quad:
    b = lerp(approach(0), 1.0, Options.stage_cover)
    return perspective_rect(
        l=-6,
        r=6,
        t=LANE_T,
        b=b,
    )


def layout_hidden_cover() -> Quad:
    b = 1 - NOTE_H
    t = min(b, max(lerp(1.0, approach(0), Options.hidden), lerp(approach(0), 1.0, Options.stage_cover)))
    return perspective_rect(
        l=-6,
        r=6,
        t=t,
        b=b,
    )


def layout_fallback_judge_line() -> Quad:
    return perspective_rect(l=-6, r=6, t=1 - NOTE_H, b=1 + NOTE_H)


def layout_note_body_by_edges(l: float, r: float, h: float, travel: float):
    if Options.alternative_approach_curve:
        offset = 80
        test_offset = 0.5
        current_d = 1 / travel + offset
        current_d_offset = current_d + test_offset
        current_h = 1 / current_d - 1 / current_d_offset
        reference_d = 1 + offset
        reference_d_offset = reference_d + test_offset
        reference_h = 1 / reference_d - 1 / reference_d_offset
        h *= current_h / reference_h
    return perspective_rect(l=l, r=r, t=1 - h, b=1 + h, travel=travel)


def layout_note_body_slices_by_edges(
    l: float, r: float, h: float, edge_w: float, travel: float
) -> tuple[Quad, Quad, Quad]:
    m = (l + r) / 2
    if r < l:
        # Make the note 0 width; shouldn't normally happen, but in case, we want to handle it gracefully
        l = r = m
    ml = min(l + edge_w, m)
    mr = max(r - edge_w, m)
    return (
        layout_note_body_by_edges(l=l, r=ml, h=h, travel=travel),
        layout_note_body_by_edges(l=ml, r=mr, h=h, travel=travel),
        layout_note_body_by_edges(l=mr, r=r, h=h, travel=travel),
    )


def layout_regular_note_body(lane: float, size: float, travel: float) -> tuple[Quad, Quad, Quad]:
    return layout_note_body_slices_by_edges(
        l=lane - size + Options.note_margin,
        r=lane + size - Options.note_margin,
        h=NOTE_H,
        edge_w=NOTE_EDGE_W,
        travel=travel,
    )


def layout_regular_note_body_fallback(lane: float, size: float, travel: float) -> Quad:
    return layout_note_body_by_edges(
        l=lane - size + Options.note_margin,
        r=lane + size - Options.note_margin,
        h=NOTE_H,
        travel=travel,
    )


def layout_slim_note_body(lane: float, size: float, travel: float) -> tuple[Quad, Quad, Quad]:
    return layout_note_body_slices_by_edges(
        l=lane - size + Options.note_margin,
        r=lane + size - Options.note_margin,
        h=NOTE_H,  # Height is handled by the sprite rather than being changed here
        edge_w=NOTE_SLIM_EDGE_W,
        travel=travel,
    )


def layout_slim_note_body_fallback(lane: float, size: float, travel: float) -> Quad:
    return layout_note_body_by_edges(
        l=lane - size + Options.note_margin,
        r=lane + size - Options.note_margin,
        h=NOTE_H / 2,  # For fallback, we need to halve the height manually engine-side
        travel=travel,
    )


def layout_tick(lane: float, travel: float) -> Rect:
    center = transform_vec(Vec2(lane, 1) * travel)
    return Rect.from_center(center, Vec2(Layout.scaled_note_h, Layout.scaled_note_h) * -2 * travel)


def layout_flick_arrow(
    lane: float, size: float, direction: FlickDirection, travel: float, animation_progress: float
) -> Quad:
    match direction:
        case FlickDirection.UP_OMNI:
            is_down = False
            reverse = False
            animation_top_x_offset = 0
        case FlickDirection.DOWN_OMNI:
            is_down = True
            reverse = False
            animation_top_x_offset = 0
        case FlickDirection.UP_LEFT:
            is_down = False
            reverse = False
            animation_top_x_offset = -1
        case FlickDirection.UP_RIGHT:
            is_down = False
            reverse = True
            animation_top_x_offset = 1
        case FlickDirection.DOWN_LEFT:
            is_down = True
            reverse = False
            animation_top_x_offset = 1
        case FlickDirection.DOWN_RIGHT:
            is_down = True
            reverse = True
            animation_top_x_offset = -1
        case _:
            assert_never(direction)
    w = clamp(size, 0, 3) / 2
    base_bl = transform_vec(Vec2(lane - w, 1) * travel)
    base_br = transform_vec(Vec2(lane + w, 1) * travel)
    up = (base_br - base_bl).rotate(pi / 2)
    base_tl = base_bl + up
    base_tr = base_br + up
    offset_scale = animation_progress if not is_down else 1 - animation_progress
    offset = Vec2(animation_top_x_offset * Layout.w_scale, 2 * Layout.w_scale) * offset_scale * travel
    result = Quad(
        bl=base_bl,
        br=base_br,
        tl=base_tl,
        tr=base_tr,
    ).translate(offset)
    if reverse:
        swap(result.bl, result.br)
        swap(result.tl, result.tr)
    return result


def layout_flick_arrow_fallback(
    lane: float, size: float, direction: FlickDirection, travel: float, animation_progress: float
) -> Quad:
    match direction:
        case FlickDirection.UP_OMNI:
            rotation = 0
            animation_top_x_offset = 0
            is_down = False
        case FlickDirection.DOWN_OMNI:
            rotation = pi
            animation_top_x_offset = 0
            is_down = True
        case FlickDirection.UP_LEFT:
            rotation = pi / 6
            animation_top_x_offset = -1
            is_down = False
        case FlickDirection.UP_RIGHT:
            rotation = -pi / 6
            animation_top_x_offset = 1
            is_down = False
        case FlickDirection.DOWN_LEFT:
            rotation = pi * 5 / 6
            animation_top_x_offset = 1
            is_down = True
            lane -= 0.25  # Note: backwards from the regular skin due to how the sprites are designed
        case FlickDirection.DOWN_RIGHT:
            rotation = -pi * 5 / 6
            animation_top_x_offset = -1
            is_down = True
            lane += 0.25
        case _:
            assert_never(direction)

    w = clamp(size / 2, 1, 2)
    offset_scale = animation_progress if not is_down else 1 - animation_progress
    offset = Vec2(animation_top_x_offset * Layout.w_scale, 2 * Layout.w_scale) * offset_scale * travel
    return (
        Rect(l=-1, r=1, t=1, b=-1)
        .as_quad()
        .rotate(rotation)
        .scale(Vec2(w, w) * Layout.w_scale * travel)
        .translate(transform_vec(Vec2(lane, 1) * travel))
        .translate(offset)
    )


def layout_slot_effect(lane: float) -> Quad:
    return perspective_rect(
        l=lane - 0.5,
        r=lane + 0.5,
        b=1 + NOTE_H,
        t=1 - NOTE_H,
    )


def layout_slot_glow_effect(lane: float, size: float, height: float) -> Quad:
    s = 1 + 0.25 * Options.slot_effect_size
    h = 4.25 * Layout.w_scale * Options.slot_effect_size
    l_min = transform_vec(Vec2(lane - size, 1))
    r_min = transform_vec(Vec2(lane + size, 1))
    l_max = (l_min + Vec2(0, h)) * Vec2(s, 1)
    r_max = (r_min + Vec2(0, h)) * Vec2(s, 1)
    return Quad(
        bl=l_min,
        br=r_min,
        tl=lerp(l_min, l_max, height),
        tr=lerp(r_min, r_max, height),
    )


def layout_linear_effect(lane: float, shear: float) -> Quad:
    w = Options.note_effect_size
    bl = transform_vec(Vec2(lane - w, 1))
    br = transform_vec(Vec2(lane + w, 1))
    up = (br - bl).rotate(pi / 2) + (shear + 0.125 * lane) * (br - bl) / 2
    return Quad(
        bl=bl,
        br=br,
        tl=bl + up,
        tr=br + up,
    )


def layout_rotated_linear_effect(lane: float, shear: float) -> Quad:
    w = Options.note_effect_size
    bl = transform_vec(Vec2(lane - w, 1))
    br = transform_vec(Vec2(lane + w, 1))
    up = (br - bl).orthogonal()
    return Quad(
        bl=bl,
        br=br,
        tl=bl + up,
        tr=br + up,
    ).rotate_about(atan(-(shear + 0.125 * lane) / 2), pivot=(bl + br) / 2)


def layout_circular_effect(lane: float, w: float, h: float) -> Quad:
    w *= Options.note_effect_size
    h *= Options.note_effect_size * Layout.w_scale / Layout.h_scale
    t = 1 + h
    b = 1 - h
    return transform_quad(
        Quad(
            bl=Vec2(lane * b - w, b),
            br=Vec2(lane * b + w, b),
            tl=Vec2(lane * t - w, t),
            tr=Vec2(lane * t + w, t),
        )
    )


def layout_tick_effect(lane: float) -> Rect:
    w = 4 * Layout.w_scale * Options.note_effect_size
    h = w
    center = transform_vec(Vec2(lane, 1))
    return Rect(
        l=center.x - w,
        r=center.x + w,
        t=center.y + h,
        b=center.y - h,
    )


def layout_slide_connector_segment(
    start_lane: float,
    start_size: float,
    start_travel: float,
    end_lane: float,
    end_size: float,
    end_travel: float,
) -> Quad:
    if start_travel < end_travel:
        start_lane, end_lane = end_lane, start_lane
        start_size, end_size = end_size, start_size
        start_travel, end_travel = end_travel, start_travel
    return transform_quad(
        Quad(
            bl=Vec2(start_lane - start_size, 1) * start_travel,
            br=Vec2(start_lane + start_size, 1) * start_travel,
            tl=Vec2(end_lane - end_size, 1) * end_travel,
            tr=Vec2(end_lane + end_size, 1) * end_travel,
        )
    )


def layout_sim_line(
    left_lane: float,
    left_travel: float,
    right_lane: float,
    right_travel: float,
) -> Quad:
    if left_lane > right_lane:
        left_lane, right_lane = right_lane, left_lane
        left_travel, right_travel = right_travel, left_travel
    ml = perspective_vec(left_lane, 1, left_travel)
    mr = perspective_vec(right_lane, 1, right_travel)
    ort = (mr - ml).orthogonal().normalize()
    return Quad(
        bl=ml + ort * NOTE_H * Layout.h_scale * left_travel,
        br=mr + ort * NOTE_H * Layout.h_scale * right_travel,
        tl=ml - ort * NOTE_H * Layout.h_scale * left_travel,
        tr=mr - ort * NOTE_H * Layout.h_scale * right_travel,
    )


def layout_hitbox(
    l: float,
    r: float,
) -> Rect:
    bl = transform_vec(Vec2(l, LANE_HITBOX_B))
    tr = transform_vec(Vec2(r, LANE_HITBOX_T))
    return Rect(l=bl.x, r=tr.x, b=bl.y, t=tr.y)


def iter_slot_lanes(lane: float, size: float):
    for i in range(floor(lane - size), ceil(lane + size)):
        yield i + 0.5
