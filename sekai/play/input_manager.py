from __future__ import annotations

from sonolus.script.archetype import PlayArchetype, callback
from sonolus.script.array import Dim
from sonolus.script.containers import ArrayMap, ArraySet
from sonolus.script.globals import level_memory
from sonolus.script.runtime import Touch, touches

from sekai.lib import archetype_names
from sekai.lib.buckets import SLIDE_END_LOCKOUT_DURATION
from sekai.lib.layout import layout_hitbox
from sekai.lib.note import get_leniency, is_head
from sekai.play import note

# Notes within this threshold in seconds of each other in target time are considered simultaneous
# when it comes to hitbox conflict resolution.
SIMULTANEOUS_THRESHOLD = 0.002


@level_memory
class InputState:
    disallowed_empty_touches: ArraySet[int, Dim[32]]
    disallowed_release_touches: ArrayMap[int, float, Dim[32]]
    last_started_touch_id: int
    last_started_touch_disallowed: bool
    previous_touch_disallowed: bool


def disallow_empty(touch: Touch):
    InputState.disallowed_empty_touches.add(touch.id)
    if touch.id == InputState.last_started_touch_id or touch.started:
        InputState.last_started_touch_disallowed = True


def disallow_release(touch: Touch, until_time: float):
    if touch.id in InputState.disallowed_release_touches:
        until_time = max(InputState.disallowed_release_touches[touch.id], until_time)
    InputState.disallowed_release_touches[touch.id] = until_time


def is_allowed_empty(touch: Touch) -> bool:
    return touch.id not in InputState.disallowed_empty_touches


def is_allowed_release(touch: Touch, target_time: float) -> bool:
    if touch.id not in InputState.disallowed_release_touches:
        return True
    return InputState.disallowed_release_touches[touch.id] <= target_time


class InputManager(PlayArchetype):
    name = archetype_names.INPUT_MANAGER

    @callback(order=-1)
    def update_sequential(self):
        note.NoteMemory.active_tap_input_notes.clear()
        note.NoteMemory.active_release_input_notes.clear()

    @callback(order=-1)
    def touch(self):
        update_input_state()
        preassign_taps()
        preassign_releases()


def update_input_state():
    old_disallowed_empty_touches = +InputState.disallowed_empty_touches
    InputState.disallowed_empty_touches.clear()

    old_disallowed_release_touches = +InputState.disallowed_release_touches
    InputState.disallowed_release_touches.clear()

    for touch in touches():
        if touch.started:
            InputState.previous_touch_disallowed = InputState.last_started_touch_disallowed

            InputState.last_started_touch_id = touch.id
            InputState.last_started_touch_disallowed = False

            InputState.last_started_touch_id = touch.id

        if touch.id in old_disallowed_empty_touches:
            disallow_empty(touch)

        if touch.id in old_disallowed_release_touches:
            InputState.disallowed_release_touches[touch.id] = old_disallowed_release_touches[touch.id]


def is_last_started_touch_disallowed() -> bool:
    return InputState.last_started_touch_disallowed

def is_previous_touch_disallowed() -> bool:
    return InputState.previous_touch_disallowed


def preassign_taps():
    active_input_taps = note.NoteMemory.active_tap_input_notes
    active_input_taps.sort(key=lambda ref: ref.get().target_time)
    available_tap_indexes = ArraySet[int, Dim[32]].new()
    for i, touch in enumerate(touches()):
        if touch.started:
            available_tap_indexes.add(i)
    for current_i in range(len(active_input_taps)):
        current = active_input_taps[current_i].get()
        for use_leniency in (False, True):
            if current.captured_touch_id != 0:
                continue
            leniency = get_leniency(current.kind) if use_leniency else 0.0
            current_l = current.lane - current.size
            current_r = current.lane + current.size
            hitbox_l = current_l - leniency
            hitbox_r = current_r + leniency
            # Earlier notes have already been processed — if they could capture a tap,
            # they would have done so already.
            for other_i in range(current_i + 1, len(active_input_taps)):
                other = active_input_taps[other_i].get()
                if other.target_time - current.target_time > SIMULTANEOUS_THRESHOLD:
                    # Since the notes are sorted by target time, we can stop checking further
                    break
                if other.captured_touch_id != 0:
                    continue
                other_l = other.lane - other.size
                other_r = other.lane + other.size
                if other_l < current_l:
                    hitbox_l = max(hitbox_l, (current_l + other_r) / 2)
                if other_r > current_r:
                    hitbox_r = min(hitbox_r, (current_r + other_l) / 2)
            if use_leniency:
                hitbox_l = min(hitbox_l, current_l)
                hitbox_r = max(hitbox_r, current_r)
            hitbox_layout = layout_hitbox(hitbox_l, hitbox_r)
            for tap_i in available_tap_indexes:
                touch = touches()[tap_i]
                if hitbox_layout.contains_point(touch.position) and touch.time in current.unadjusted_input_interval:
                    disallow_empty(touch)
                    if not is_head(current.kind):
                        disallow_release(touch, current.target_time + SLIDE_END_LOCKOUT_DURATION)
                    current.captured_touch_id = touch.id
                    current.captured_touch_time = min(touch.time, touch.start_time)
                    available_tap_indexes.remove(tap_i)
                    break


def preassign_releases():
    active_input_releases = note.NoteMemory.active_release_input_notes
    active_input_releases.sort(key=lambda ref: ref.get().target_time)
    active_release_indexes = ArraySet[int, Dim[32]].new()
    for i, touch in enumerate(touches()):
        if touch.ended:
            active_release_indexes.add(i)
    for current_i in range(len(active_input_releases)):
        current = active_input_releases[current_i].get()
        for use_leniency in (False, True):
            if current.captured_touch_id != 0:
                continue
            leniency = get_leniency(current.kind) if use_leniency else 0.0
            current_l = current.lane - current.size
            current_r = current.lane + current.size
            hitbox_l = current_l - leniency
            hitbox_r = current_r + leniency
            for other_i in range(current_i + 1, len(active_input_releases)):
                other = active_input_releases[other_i].get()
                if other.target_time - current.target_time > SIMULTANEOUS_THRESHOLD:
                    break
                if other.captured_touch_id != 0:
                    continue
                other_l = other.lane - other.size
                other_r = other.lane + other.size
                if other_l < current_l:
                    hitbox_l = max(hitbox_l, (current_l + other_r) / 2)
                if other_r > current_r:
                    hitbox_r = min(hitbox_r, (current_r + other_l) / 2)
            if use_leniency:
                hitbox_l = min(hitbox_l, current_l)
                hitbox_r = max(hitbox_r, current_r)
            hitbox_layout = layout_hitbox(hitbox_l, hitbox_r)
            for release_i in active_release_indexes:
                touch = touches()[release_i]
                if current.active_head_ref.index > 0:
                    active_connector_info = current.active_head_ref.get().active_connector_info
                    connector_hitbox = active_connector_info.get_hitbox(get_leniency(current.kind))
                    ignore_lockout = not any(
                        not t.ended and connector_hitbox.contains_point(t.position) for t in touches()
                    )
                else:
                    ignore_lockout = False
                if (
                    hitbox_layout.contains_point(touch.position)
                    and (ignore_lockout or is_allowed_release(touch, current.target_time))
                    and touch.time in current.unadjusted_input_interval
                ):
                    disallow_empty(touch)
                    current.captured_touch_id = touch.id
                    current.captured_touch_time = touch.time  # Unused currently, but set for consistency
                    active_release_indexes.remove(release_i)
                    break
