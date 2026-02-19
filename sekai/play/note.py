from __future__ import annotations

from math import pi
from typing import assert_never, cast

from sonolus.script.archetype import (
    AnyArchetype,
    EntityRef,
    PlayArchetype,
    StandardImport,
    entity_data,
    entity_memory,
    exported,
    imported,
    shared_memory,
)
from sonolus.script.array import Dim
from sonolus.script.bucket import Judgment
from sonolus.script.containers import VarArray
from sonolus.script.globals import level_memory
from sonolus.script.interval import Interval, remap_clamped, unlerp_clamped
from sonolus.script.quad import Rect
from sonolus.script.runtime import Touch, delta_time, input_offset, offset_adjusted_time, time, touches
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.buckets import WINDOW_SCALE, SekaiWindow
from sekai.lib.connector import ActiveConnectorInfo, ConnectorKind, ConnectorLayer
from sekai.lib.ease import EaseType
from sekai.lib.layout import FlickDirection, Layout, layout_hitbox, layout_lane, progress_to
from sekai.lib.note import (
    NoteEffectKind,
    NoteKind,
    draw_note,
    get_attach_params,
    get_leniency,
    get_note_bucket,
    get_note_effect_kind,
    get_note_haptic_feedback,
    get_note_particles,
    get_note_window,
    get_visual_spawn_time,
    has_release_input,
    has_tap_input,
    is_head,
    map_note_kind,
    mirror_flick_direction,
    play_note_hit_effects,
    schedule_note_auto_sfx,
)
from sekai.lib.options import Options
from sekai.lib.particle import BaseParticles
from sekai.lib.timescale import CompositeTime, group_hide_notes, group_scaled_time, group_time_to_scaled_time
from sekai.play import input_manager
from sekai.play.common import PlayLevelMemory
from sekai.play.custom_elements import spawn_custom
from sekai.play.events import SkillActive
from sekai.play.particle_manager import ParticleManager

DEFAULT_BEST_TOUCH_TIME = -1e8


class BaseNote(PlayArchetype):
    beat: StandardImport.BEAT
    timescale_group: StandardImport.TIMESCALE_GROUP
    lane: float = imported()
    size: float = imported()
    direction: FlickDirection = imported()
    active_head_ref: EntityRef[BaseNote] = imported(name="activeHead")
    is_attached: bool = imported(name="isAttached")
    connector_ease: EaseType = imported(name="connectorEase")
    segment_kind: ConnectorKind = imported(name="segmentKind")
    segment_alpha: float = imported(name="segmentAlpha")
    segment_layer: ConnectorLayer = imported(name="segmentLayer")
    attach_head_ref: EntityRef[BaseNote] = imported(name="attachHead")
    attach_tail_ref: EntityRef[BaseNote] = imported(name="attachTail")
    next_ref: EntityRef[BaseNote] = imported(name="next")  # Only for level data; not used in-game.
    effect_kind: NoteEffectKind = imported(name="effectKind")

    kind: NoteKind = entity_data()
    data_init_done: bool = entity_data()
    target_time: float = entity_data()
    visual_start_time: float = entity_data()
    start_time: float = entity_data()
    target_scaled_time: CompositeTime = entity_data()

    judgment_window: SekaiWindow = shared_memory()
    input_interval: Interval = shared_memory()
    unadjusted_input_interval: Interval = shared_memory()

    # The id of the tap that activated this note, for tap notes and flicks or released the note, for release notes.
    # This is set by the input manager rather than the note itself.
    captured_touch_id: int = shared_memory()
    captured_touch_time: float = shared_memory()
    tick_head_ref: EntityRef[BaseNote] = shared_memory()
    tick_tail_ref: EntityRef[BaseNote] = shared_memory()

    active_connector_info: ActiveConnectorInfo = shared_memory()

    count: int = shared_memory()

    # For trace early touches
    best_touch_time: float = entity_memory()
    best_touch_matches_direction: bool = entity_memory()

    should_play_hit_effects: bool = entity_memory()

    # Check wrong way
    wrong_way: bool = entity_memory()
    wrong_way_check: bool = exported()

    end_time: float = exported()
    played_hit_effects: bool = exported()

    # cache
    hitbox: Rect = entity_memory()
    target_angle: float = entity_memory()
    direction_check_needed: bool = entity_memory()
    attach_frac: float = shared_memory()

    def init_data(self):
        if self.data_init_done:
            return

        self.kind = map_note_kind(cast(NoteKind, self.key))
        self.effect_kind = get_note_effect_kind(self.kind, self.effect_kind)

        self.data_init_done = True

        if Options.mirror:
            self.lane *= -1
            self.direction = mirror_flick_direction(self.direction)

        self.target_time = beat_to_time(self.beat)
        self.judgment_window = get_note_window(self.kind)
        self.input_interval = self.judgment_window.bad + self.target_time + input_offset()
        self.unadjusted_input_interval = self.judgment_window.bad + self.target_time

        if not self.is_attached:
            self.target_scaled_time = group_time_to_scaled_time(self.timescale_group, self.target_time)
            self.visual_start_time = get_visual_spawn_time(self.timescale_group, self.target_scaled_time)
            self.start_time = min(self.visual_start_time, self.input_interval.start)

    def preprocess(self):
        self.init_data()

        self.result.bucket = get_note_bucket(self.kind)

        self.best_touch_time = DEFAULT_BEST_TOUCH_TIME

        if self.is_attached:
            attach_head = self.attach_head_ref.get()
            attach_tail = self.attach_tail_ref.get()
            attach_head.init_data()
            attach_tail.init_data()
            self.connector_ease = attach_head.connector_ease
            lane, size = get_attach_params(
                ease_type=attach_head.connector_ease,
                head_lane=attach_head.lane,
                head_size=attach_head.size,
                head_target_time=attach_head.target_time,
                tail_lane=attach_tail.lane,
                tail_size=attach_tail.size,
                tail_target_time=attach_tail.target_time,
                target_time=self.target_time,
            )
            self.lane = lane
            self.size = size
            self.visual_start_time = min(attach_head.visual_start_time, attach_tail.visual_start_time)
            self.start_time = min(self.visual_start_time, self.input_interval.start)
            self.attach_frac = unlerp_clamped(attach_head.target_time, attach_tail.target_time, self.target_time)

        if is_head(self.kind):
            self.active_connector_info.input_lane = self.lane
            self.active_connector_info.input_size = self.size

        if self.is_scored:
            schedule_note_auto_sfx(self.effect_kind, self.target_time)

        # caching
        leniency = get_leniency(self.kind)
        self.hitbox = layout_hitbox(self.lane - self.size - leniency, self.lane + self.size + leniency)

        match self.direction:
            case FlickDirection.UP_OMNI | FlickDirection.DOWN_OMNI:
                self.direction_check_needed = False
                self.target_angle = 0
            case FlickDirection.UP_LEFT:
                self.direction_check_needed = True
                self.target_angle = pi / 2 + 1
            case FlickDirection.UP_RIGHT:
                self.direction_check_needed = True
                self.target_angle = pi / 2 - 1
            case FlickDirection.DOWN_LEFT:
                self.direction_check_needed = True
                self.target_angle = -pi / 2 - 1
            case FlickDirection.DOWN_RIGHT:
                self.direction_check_needed = True
                self.target_angle = -pi / 2 + 1
            case _:
                self.direction_check_needed = False
                self.target_angle = 0

    def spawn_order(self) -> float:
        if self.kind == NoteKind.ANCHOR:
            return 1e8
        return self.start_time

    def should_spawn(self) -> bool:
        if self.kind == NoteKind.ANCHOR:
            return False
        return time() >= self.start_time

    @property
    def calc_time(self) -> float:
        return self.target_time

    def update_sequential(self):
        if self.despawn:
            return
        if self.should_do_delayed_trigger():
            if self.best_touch_matches_direction:
                self.judge(self.best_touch_time)
            else:
                self.judge_wrong_way(self.best_touch_time)
            return
        if self.tick_trigger():
            self.complete()
            return
        if self.is_scored and time() in self.input_interval and self.captured_touch_id == 0:
            if has_tap_input(self.kind):
                NoteMemory.active_tap_input_notes.append(self.ref())
            elif has_release_input(self.kind) and (
                self.active_head_ref.index <= 0
                or self.active_head_ref.get().is_despawned
                or self.active_head_ref.get().captured_touch_id != 0
                or not self.active_head_ref.get().is_scored
            ):
                NoteMemory.active_release_input_notes.append(self.ref())

    def touch(self):
        if not self.is_scored:
            return
        if self.despawn:
            return
        if time() < self.input_interval.start:
            return
        kind = self.kind
        match kind:
            case (
                NoteKind.NORM_TAP
                | NoteKind.CRIT_TAP
                | NoteKind.NORM_HEAD_TAP
                | NoteKind.CRIT_HEAD_TAP
                | NoteKind.NORM_TAIL_TAP
                | NoteKind.CRIT_TAIL_TAP
            ):
                self.handle_tap_input()
            case NoteKind.NORM_FLICK | NoteKind.CRIT_FLICK | NoteKind.NORM_HEAD_FLICK | NoteKind.CRIT_HEAD_FLICK:
                self.handle_flick_input()
            case (
                NoteKind.NORM_TRACE
                | NoteKind.CRIT_TRACE
                | NoteKind.NORM_HEAD_TRACE
                | NoteKind.CRIT_HEAD_TRACE
                | NoteKind.NORM_TAIL_TRACE
                | NoteKind.CRIT_TAIL_TRACE
            ):
                self.handle_trace_input()
            case (
                NoteKind.NORM_TRACE_FLICK
                | NoteKind.CRIT_TRACE_FLICK
                | NoteKind.NORM_HEAD_TRACE_FLICK
                | NoteKind.CRIT_HEAD_TRACE_FLICK
            ):
                self.handle_trace_flick_input()
            case (
                NoteKind.NORM_TAIL_FLICK
                | NoteKind.CRIT_TAIL_FLICK
                | NoteKind.NORM_TAIL_TRACE_FLICK
                | NoteKind.CRIT_TAIL_TRACE_FLICK
            ):
                self.handle_trace_flick_input()
            case (
                NoteKind.NORM_RELEASE
                | NoteKind.CRIT_RELEASE
                | NoteKind.NORM_HEAD_RELEASE
                | NoteKind.CRIT_HEAD_RELEASE
                | NoteKind.NORM_TAIL_RELEASE
                | NoteKind.CRIT_TAIL_RELEASE
            ):
                self.handle_release_input()
            case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK:
                self.handle_tick_input()
            case NoteKind.DAMAGE:
                self.handle_damage_input()
            case NoteKind.ANCHOR:
                pass
            case _:
                assert_never(kind)

    def update_parallel(self):
        if self.despawn:
            return
        if not self.is_scored and time() >= self.target_time:
            self.despawn = True
            return
        if time() < self.visual_start_time:
            return
        if time() > self.input_interval.end:
            self.handle_late_miss()
            return
        if is_head(self.kind) and time() > self.target_time:
            return
        if group_hide_notes(self.timescale_group):
            return
        if Options.disable_fake_notes and not self.is_scored:
            return
        draw_note(self.kind, self.lane, self.size, self.progress, self.direction, self.target_time)

    def tick_trigger(self):
        return (
            self.kind in (NoteKind.NORM_TICK, NoteKind.CRIT_TICK)
            and (
                (
                    not self.is_attached
                    and (
                        (
                            self.tick_head_ref.index > 0
                            and (
                                self.tick_head_ref.get().active_connector_info.is_active
                                and time() >= self.input_interval.start
                            )
                        )
                        or (self.tick_tail_ref.index > 0 and self.tick_tail_ref.get().is_despawned)
                    )
                )
                or (
                    self.is_attached
                    and (
                        (
                            self.attach_head_ref.get().tick_head_ref.index > 0
                            and (
                                self.attach_head_ref.get().tick_head_ref.get().active_connector_info.is_active
                                and time() >= self.input_interval.start
                            )
                        )
                        or (
                            self.attach_head_ref.get().tick_tail_ref.index > 0
                            and self.attach_head_ref.get().tick_tail_ref.get().is_despawned
                        )
                    )
                )
            )
        ) or (
            self.kind == NoteKind.HIDE_TICK
            and self.attach_head_ref.index > 0
            and self.attach_head_ref.get().tick_tail_ref.index > 0
            and (
                self.attach_head_ref.get().tick_tail_ref.get().is_despawned
                or (
                    self.attach_head_ref.get().tick_tail_ref.get().kind == NoteKind.ANCHOR
                    and time() >= self.attach_head_ref.get().tick_tail_ref.get().target_time
                )
                or (
                    self.attach_head_ref.get().tick_head_ref.get().active_connector_info.is_active
                    and time() >= self.input_interval.start
                )
            )
        )

    def should_do_delayed_trigger(self) -> bool:
        # Don't trigger if the previous frame was before the target time.
        # This gives the regular touch handling a chance to trigger on time the first time we pass the target time.
        if offset_adjusted_time() - delta_time() <= self.target_time and time() < self.input_interval.end:
            return False

        # Don't trigger if we never had a touch recorded.
        if self.best_touch_time == DEFAULT_BEST_TOUCH_TIME:
            return False

        # Give until the end of the perfect window to give a right-way touch if we've only had wrong-way touches.
        # After that, wrong-way has no impact anyway.
        # If we get a wrong-way touch after the target time, we will still trigger immediately from the touch
        # callback though.
        if (
            not self.best_touch_matches_direction
            and offset_adjusted_time() < self.target_time + self.judgment_window.perfect.end
        ):
            return False

        # If a new input could improve the judgment...
        if offset_adjusted_time() < self.target_time + (self.target_time - self.best_touch_time):
            # If we're still in the perfect window, wait for it to end.
            if offset_adjusted_time() < self.target_time + self.judgment_window.perfect.end:
                return False
            # Otherwise, see if there's any ongoing touches in the hitbox.
            hitbox = self.get_full_hitbox()
            for touch in touches():
                if not touch.ended and hitbox.contains_point(touch.position):
                    return False
            # If we're past the perfect window, and there are no ongoing touches in the hitbox, we can trigger to
            # avoid delaying the trigger by too long.
        return True

    def terminate(self):
        if self.should_play_hit_effects:
            # We do this here for parallelism, and to reduce compilation time.
            play_note_hit_effects(
                self.kind,
                self.effect_kind,
                self.lane,
                self.size,
                self.direction,
                self.result.judgment,
            )
            if Options.lane_effect_enabled:
                particles = get_note_particles(self.kind, self.direction)
                if particles.lane.id == BaseParticles.critical_flick_note_lane_linear.id:
                    layout = layout_lane(self.lane, self.size)
                    ParticleManager.spawn(
                        particle=particles.lane.spawn(layout, duration=1 / Options.effect_animation_speed),
                        lane=self.lane,
                        spawn_time=time(),
                    )
        if self.is_scored:
            self.result.haptic = get_note_haptic_feedback(self.kind, self.result.judgment)
        self.end_time = offset_adjusted_time()
        self.played_hit_effects = self.should_play_hit_effects
        if self.is_scored:
            self.wrong_way_check = self.wrong_way
            spawn_custom(
                judgment=self.result.judgment,
                accuracy=self.result.accuracy,
                windows=self.judgment_window,
                wrong_way=self.wrong_way,
                target_time=self.target_time,
                index=self.index,
                played_hit_effects=self.should_play_hit_effects,
            )

    def handle_tap_input(self):
        if time() > self.input_interval.end:
            return

        hitbox = self.get_full_hitbox()
        for empty_touch in touches():
            if hitbox.contains_point(empty_touch.position) and empty_touch.started:
                input_manager.disallow_empty(empty_touch)

        if self.captured_touch_id == 0:
            return
        touch = next(tap for tap in touches() if tap.id == self.captured_touch_id)
        self.judge(touch.start_time)

    def handle_release_input(self):
        if time() > self.input_interval.end:
            return
        if self.captured_touch_id == 0:
            return
        touch = next(tap for tap in touches() if tap.id == self.captured_touch_id)
        self.judge(touch.time)

    def handle_flick_input(self):
        if time() > self.input_interval.end:
            return
        if self.captured_touch_id == 0:
            return

        # Another touch is allowed to flick the note as long as it started after the start of the input interval,
        # so we don't care which touch matched the tap id, just that the tap id is set.

        hitbox = self.get_full_hitbox()

        for touch in touches():
            if hitbox.contains_point(touch.position) and touch.started:
                input_manager.disallow_empty(touch)
            if not self.check_touch_touch_is_eligible_for_flick(hitbox, touch):
                continue
            if not self.check_direction_matches(touch.angle):
                continue
            self.judge(touch.time)
            return
        for touch in touches():
            if not self.check_touch_touch_is_eligible_for_flick(hitbox, touch):
                continue
            self.judge_wrong_way(touch.time)
            return

    def handle_trace_input(self):
        if time() > self.input_interval.end:
            return
        if self.should_do_delayed_trigger():
            return
        hitbox = self.get_full_hitbox()
        has_touch = False
        for touch in touches():
            if not self.check_touch_is_eligible_for_trace(hitbox, touch):
                continue
            input_manager.disallow_empty(touch)
            has_touch = True
            # Keep going so we disallow empty on all touches that are in the hitbox.
        if not has_touch:
            return
        if offset_adjusted_time() >= self.target_time:
            if offset_adjusted_time() - delta_time() <= self.target_time <= offset_adjusted_time():
                self.complete()
            else:
                self.judge(offset_adjusted_time())
        else:
            self.best_touch_time = offset_adjusted_time()
            self.best_touch_matches_direction = True

    def handle_trace_flick_input(self):
        if time() > self.input_interval.end:
            return
        if self.should_do_delayed_trigger():
            return
        hitbox = self.get_full_hitbox()
        has_touch = False
        has_correct_direction_touch = False
        for touch in touches():
            if not self.check_touch_is_eligible_for_trace(hitbox, touch):
                continue
            input_manager.disallow_empty(touch)
            if not self.check_touch_is_eligible_for_trace_flick(hitbox, touch):
                continue
            has_touch = True
            if self.check_direction_matches(touch.angle):
                has_correct_direction_touch = True
        if not has_touch:
            return
        if offset_adjusted_time() >= self.target_time:
            if offset_adjusted_time() - delta_time() <= self.target_time <= offset_adjusted_time():
                if has_correct_direction_touch:
                    self.complete()
                else:
                    self.complete_wrong_way()
            elif has_correct_direction_touch:
                self.judge(offset_adjusted_time())
            else:
                self.judge_wrong_way(offset_adjusted_time())
        elif (
            has_correct_direction_touch or self.best_touch_time < self.judgment_window.perfect.start + self.target_time
        ):
            self.best_touch_time = offset_adjusted_time()
            self.best_touch_matches_direction = has_correct_direction_touch

    def handle_tick_input(self):
        hitbox = self.get_full_hitbox()
        for touch in touches():
            if not hitbox.contains_point(touch.position):
                continue
            input_manager.disallow_empty(touch)
            self.complete()

    def handle_damage_input(self):
        hitbox = self.get_full_hitbox()
        has_touch = False
        for touch in touches():
            if not hitbox.contains_point(touch.position):
                continue
            input_manager.disallow_empty(touch)
            has_touch = True
        if has_touch:
            self.fail_damage()
        else:
            self.complete_damage()

    def handle_late_miss(self):
        kind = self.kind
        match kind:
            case NoteKind.NORM_TICK | NoteKind.CRIT_TICK | NoteKind.HIDE_TICK:
                self.fail_late(0.125)
            case NoteKind.DAMAGE:
                self.complete_damage()
            case (
                NoteKind.NORM_TAP
                | NoteKind.CRIT_TAP
                | NoteKind.NORM_FLICK
                | NoteKind.CRIT_FLICK
                | NoteKind.NORM_TRACE
                | NoteKind.CRIT_TRACE
                | NoteKind.NORM_TRACE_FLICK
                | NoteKind.CRIT_TRACE_FLICK
                | NoteKind.NORM_RELEASE
                | NoteKind.CRIT_RELEASE
                | NoteKind.NORM_HEAD_TAP
                | NoteKind.CRIT_HEAD_TAP
                | NoteKind.NORM_HEAD_FLICK
                | NoteKind.CRIT_HEAD_FLICK
                | NoteKind.NORM_HEAD_TRACE
                | NoteKind.CRIT_HEAD_TRACE
                | NoteKind.NORM_HEAD_TRACE_FLICK
                | NoteKind.CRIT_HEAD_TRACE_FLICK
                | NoteKind.NORM_HEAD_RELEASE
                | NoteKind.CRIT_HEAD_RELEASE
                | NoteKind.NORM_TAIL_TAP
                | NoteKind.CRIT_TAIL_TAP
                | NoteKind.NORM_TAIL_FLICK
                | NoteKind.CRIT_TAIL_FLICK
                | NoteKind.NORM_TAIL_TRACE
                | NoteKind.CRIT_TAIL_TRACE
                | NoteKind.NORM_TAIL_TRACE_FLICK
                | NoteKind.CRIT_TAIL_TRACE_FLICK
                | NoteKind.NORM_TAIL_RELEASE
                | NoteKind.CRIT_TAIL_RELEASE
            ):
                self.fail_late()
            case NoteKind.ANCHOR:
                pass
            case _:
                assert_never(kind)

    def check_touch_touch_is_eligible_for_flick(self, hitbox: Rect, touch: Touch) -> bool:
        return (
            touch.start_time >= self.captured_touch_time
            and touch.speed >= Layout.flick_speed_threshold
            and (hitbox.contains_point(touch.position) or hitbox.contains_point(touch.prev_position))
        )

    def check_touch_is_eligible_for_trace(self, hitbox: Rect, touch: Touch) -> bool:
        # Note that this does not check the time, since time may not be updated if the touch is stationary.
        return hitbox.contains_point(touch.position)

    def check_touch_is_eligible_for_trace_flick(self, hitbox: Rect, touch: Touch) -> bool:
        return (
            touch.time >= self.unadjusted_input_interval.start
            and touch.speed >= Layout.flick_speed_threshold
            and (hitbox.contains_point(touch.position) or hitbox.contains_point(touch.prev_position))
        )

    def check_direction_matches(self, angle: float) -> bool:
        if not self.direction_check_needed:
            return True

        leniency = pi / 2
        angle_diff = abs((angle - self.target_angle + pi) % (2 * pi) - pi)
        return angle_diff <= leniency

    def judge(self, actual_time: float):
        judgment = self.judgment_window.judge(actual_time, self.target_time)
        error = self.judgment_window.bad.clamp(actual_time - self.target_time)
        self.result.judgment = judgment if not SkillActive.judgment or judgment == Judgment.MISS else Judgment.PERFECT
        self.result.accuracy = error
        if self.result.bucket.id != -1:
            self.result.bucket_value = error * WINDOW_SCALE
        self.despawn = True
        self.should_play_hit_effects = True
        self.post_judge()

    def judge_wrong_way(self, actual_time: float):
        judgment = self.judgment_window.judge(actual_time, self.target_time)
        if judgment == Judgment.PERFECT:
            judgment = Judgment.GREAT
        error = self.judgment_window.bad.clamp(actual_time - self.target_time)
        self.result.judgment = judgment if not SkillActive.judgment or judgment == Judgment.MISS else Judgment.PERFECT
        if error in self.judgment_window.perfect:
            self.result.accuracy = self.judgment_window.perfect.end
        else:
            self.result.accuracy = error
        if self.result.bucket.id != -1:
            self.result.bucket_value = error * WINDOW_SCALE
        self.despawn = True
        self.should_play_hit_effects = True
        self.wrong_way = not SkillActive.judgment and judgment != Judgment.MISS
        self.post_judge()

    def complete(self):
        self.result.judgment = Judgment.PERFECT
        self.result.accuracy = 0
        if self.result.bucket.id != -1:
            self.result.bucket_value = 0
        self.despawn = True
        self.should_play_hit_effects = True
        self.post_judge()

    def complete_wrong_way(self):
        self.result.judgment = Judgment.GREAT if not SkillActive.judgment else Judgment.PERFECT
        self.result.accuracy = self.judgment_window.good.end
        if self.result.bucket.id != -1:
            self.result.bucket_value = 0
        self.despawn = True
        self.should_play_hit_effects = True
        self.post_judge()
        self.wrong_way = not SkillActive.judgment

    def complete_damage(self):
        self.result.judgment = Judgment.PERFECT
        self.result.accuracy = 0
        if self.result.bucket.id != -1:
            self.result.bucket_value = 0
        self.despawn = True

    def fail_late(self, accuracy: float | None = None):
        if accuracy is None:
            accuracy = self.judgment_window.bad.end
        self.result.judgment = Judgment.MISS
        self.result.accuracy = accuracy
        if self.result.bucket.id != -1:
            self.result.bucket_value = self.judgment_window.bad.end * WINDOW_SCALE
        self.despawn = True

    def fail_damage(self):
        self.result.judgment = Judgment.MISS
        self.result.accuracy = 0.125
        self.despawn = True
        self.should_play_hit_effects = True
        self.post_judge()

    def post_judge(self):
        if self.should_play_hit_effects:
            PlayLevelMemory.last_note_sfx_time = time()

    def get_full_hitbox(self) -> Rect:
        return self.hitbox

    @property
    def progress(self) -> float:
        if self.is_attached:
            attach_head = self.attach_head_ref.get()
            attach_tail = self.attach_tail_ref.get()
            head_progress = (
                progress_to(attach_head.target_scaled_time, group_scaled_time(attach_head.timescale_group))
                if time() < attach_head.target_time
                else 1.0
            )
            tail_progress = progress_to(attach_tail.target_scaled_time, group_scaled_time(attach_tail.timescale_group))
            head_frac = (
                0.0
                if time() < attach_head.target_time
                else unlerp_clamped(attach_head.target_time, attach_tail.target_time, time())
            )
            tail_frac = 1.0
            frac = self.attach_frac
            return remap_clamped(head_frac, tail_frac, head_progress, tail_progress, frac)
        else:
            return progress_to(self.target_scaled_time, group_scaled_time(self.timescale_group))

    @property
    def head_ease_frac(self) -> float:
        if self.is_attached:
            return self.attach_frac
        else:
            return 0.0

    @property
    def tail_ease_frac(self) -> float:
        if self.is_attached:
            return self.attach_frac
        else:
            return 1.0

    @property
    def effective_attach_head(self) -> BaseNote:
        ref = +EntityRef[BaseNote]
        if self.is_attached:
            ref @= self.attach_head_ref
        else:
            ref @= self.ref()
        return ref.get()

    @property
    def effective_attach_tail(self) -> BaseNote:
        ref = +EntityRef[BaseNote]
        if self.is_attached:
            ref @= self.attach_tail_ref
        else:
            ref @= self.ref()
        return ref.get()


@level_memory
class NoteMemory:
    active_tap_input_notes: VarArray[EntityRef[BaseNote], Dim[256]]
    active_release_input_notes: VarArray[EntityRef[BaseNote], Dim[256]]


NormalTapNote = BaseNote.derive(archetype_names.NORMAL_TAP_NOTE, is_scored=True, key=NoteKind.NORM_TAP)
CriticalTapNote = BaseNote.derive(archetype_names.CRITICAL_TAP_NOTE, is_scored=True, key=NoteKind.CRIT_TAP)
NormalFlickNote = BaseNote.derive(archetype_names.NORMAL_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_FLICK)
CriticalFlickNote = BaseNote.derive(archetype_names.CRITICAL_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_FLICK)
NormalTraceNote = BaseNote.derive(archetype_names.NORMAL_TRACE_NOTE, is_scored=True, key=NoteKind.NORM_TRACE)
CriticalTraceNote = BaseNote.derive(archetype_names.CRITICAL_TRACE_NOTE, is_scored=True, key=NoteKind.CRIT_TRACE)
NormalTraceFlickNote = BaseNote.derive(
    archetype_names.NORMAL_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_TRACE_FLICK
)
CriticalTraceFlickNote = BaseNote.derive(
    archetype_names.CRITICAL_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_TRACE_FLICK
)
NormalReleaseNote = BaseNote.derive(archetype_names.NORMAL_RELEASE_NOTE, is_scored=True, key=NoteKind.NORM_RELEASE)
CriticalReleaseNote = BaseNote.derive(archetype_names.CRITICAL_RELEASE_NOTE, is_scored=True, key=NoteKind.CRIT_RELEASE)
NormalHeadTapNote = BaseNote.derive(archetype_names.NORMAL_HEAD_TAP_NOTE, is_scored=True, key=NoteKind.NORM_HEAD_TAP)
CriticalHeadTapNote = BaseNote.derive(
    archetype_names.CRITICAL_HEAD_TAP_NOTE, is_scored=True, key=NoteKind.CRIT_HEAD_TAP
)
NormalHeadFlickNote = BaseNote.derive(
    archetype_names.NORMAL_HEAD_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_HEAD_FLICK
)
CriticalHeadFlickNote = BaseNote.derive(
    archetype_names.CRITICAL_HEAD_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_HEAD_FLICK
)
NormalHeadTraceNote = BaseNote.derive(
    archetype_names.NORMAL_HEAD_TRACE_NOTE, is_scored=True, key=NoteKind.NORM_HEAD_TRACE
)
CriticalHeadTraceNote = BaseNote.derive(
    archetype_names.CRITICAL_HEAD_TRACE_NOTE, is_scored=True, key=NoteKind.CRIT_HEAD_TRACE
)
NormalHeadTraceFlickNote = BaseNote.derive(
    archetype_names.NORMAL_HEAD_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_HEAD_TRACE_FLICK
)
CriticalHeadTraceFlickNote = BaseNote.derive(
    archetype_names.CRITICAL_HEAD_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_HEAD_TRACE_FLICK
)
NormalHeadReleaseNote = BaseNote.derive(
    archetype_names.NORMAL_HEAD_RELEASE_NOTE, is_scored=True, key=NoteKind.NORM_HEAD_RELEASE
)
CriticalHeadReleaseNote = BaseNote.derive(
    archetype_names.CRITICAL_HEAD_RELEASE_NOTE, is_scored=True, key=NoteKind.CRIT_HEAD_RELEASE
)
NormalTailTapNote = BaseNote.derive(archetype_names.NORMAL_TAIL_TAP_NOTE, is_scored=True, key=NoteKind.NORM_TAIL_TAP)
CriticalTailTapNote = BaseNote.derive(
    archetype_names.CRITICAL_TAIL_TAP_NOTE, is_scored=True, key=NoteKind.CRIT_TAIL_TAP
)
NormalTailFlickNote = BaseNote.derive(
    archetype_names.NORMAL_TAIL_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_TAIL_FLICK
)
CriticalTailFlickNote = BaseNote.derive(
    archetype_names.CRITICAL_TAIL_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_TAIL_FLICK
)
NormalTailTraceNote = BaseNote.derive(
    archetype_names.NORMAL_TAIL_TRACE_NOTE, is_scored=True, key=NoteKind.NORM_TAIL_TRACE
)
CriticalTailTraceNote = BaseNote.derive(
    archetype_names.CRITICAL_TAIL_TRACE_NOTE, is_scored=True, key=NoteKind.CRIT_TAIL_TRACE
)
NormalTailTraceFlickNote = BaseNote.derive(
    archetype_names.NORMAL_TAIL_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.NORM_TAIL_TRACE_FLICK
)
CriticalTailTraceFlickNote = BaseNote.derive(
    archetype_names.CRITICAL_TAIL_TRACE_FLICK_NOTE, is_scored=True, key=NoteKind.CRIT_TAIL_TRACE_FLICK
)
NormalTailReleaseNote = BaseNote.derive(
    archetype_names.NORMAL_TAIL_RELEASE_NOTE, is_scored=True, key=NoteKind.NORM_TAIL_RELEASE
)
CriticalTailReleaseNote = BaseNote.derive(
    archetype_names.CRITICAL_TAIL_RELEASE_NOTE, is_scored=True, key=NoteKind.CRIT_TAIL_RELEASE
)
NormalTickNote = BaseNote.derive(archetype_names.NORMAL_TICK_NOTE, is_scored=True, key=NoteKind.NORM_TICK)
CriticalTickNote = BaseNote.derive(archetype_names.CRITICAL_TICK_NOTE, is_scored=True, key=NoteKind.CRIT_TICK)
DamageNote = BaseNote.derive(archetype_names.DAMAGE_NOTE, is_scored=True, key=NoteKind.DAMAGE)
AnchorNote = BaseNote.derive(archetype_names.ANCHOR_NOTE, is_scored=False, key=NoteKind.ANCHOR)
TransientHiddenTickNote = BaseNote.derive(
    archetype_names.TRANSIENT_HIDDEN_TICK_NOTE, is_scored=True, key=NoteKind.HIDE_TICK
)
FakeNormalTapNote = BaseNote.derive(archetype_names.FAKE_NORMAL_TAP_NOTE, is_scored=False, key=NoteKind.NORM_TAP)
FakeCriticalTapNote = BaseNote.derive(archetype_names.FAKE_CRITICAL_TAP_NOTE, is_scored=False, key=NoteKind.CRIT_TAP)
FakeNormalFlickNote = BaseNote.derive(archetype_names.FAKE_NORMAL_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_FLICK)
FakeCriticalFlickNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_FLICK_NOTE, is_scored=False, key=NoteKind.CRIT_FLICK
)
FakeNormalTraceNote = BaseNote.derive(archetype_names.FAKE_NORMAL_TRACE_NOTE, is_scored=False, key=NoteKind.NORM_TRACE)
FakeCriticalTraceNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TRACE_NOTE, is_scored=False, key=NoteKind.CRIT_TRACE
)
FakeNormalTraceFlickNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TRACE_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_TRACE_FLICK
)
FakeCriticalTraceFlickNote = BaseNote.derive(
    "FakeCriticalTraceFlickNote", is_scored=False, key=NoteKind.CRIT_TRACE_FLICK
)
FakeNormalReleaseNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_RELEASE_NOTE, is_scored=False, key=NoteKind.NORM_RELEASE
)
FakeCriticalReleaseNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_RELEASE_NOTE, is_scored=False, key=NoteKind.CRIT_RELEASE
)
FakeNormalHeadTapNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_HEAD_TAP_NOTE, is_scored=False, key=NoteKind.NORM_HEAD_TAP
)
FakeCriticalHeadTapNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_HEAD_TAP_NOTE, is_scored=False, key=NoteKind.CRIT_HEAD_TAP
)
FakeNormalHeadFlickNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_HEAD_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_HEAD_FLICK
)
FakeCriticalHeadFlickNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_HEAD_FLICK_NOTE, is_scored=False, key=NoteKind.CRIT_HEAD_FLICK
)
FakeNormalHeadTraceNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_HEAD_TRACE_NOTE, is_scored=False, key=NoteKind.NORM_HEAD_TRACE
)
FakeCriticalHeadTraceNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_HEAD_TRACE_NOTE, is_scored=False, key=NoteKind.CRIT_HEAD_TRACE
)
FakeNormalHeadTraceFlickNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_HEAD_TRACE_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_HEAD_TRACE_FLICK
)
FakeCriticalHeadTraceFlickNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_HEAD_TRACE_FLICK_NOTE, is_scored=False, key=NoteKind.CRIT_HEAD_TRACE_FLICK
)
FakeNormalHeadReleaseNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_HEAD_RELEASE_NOTE, is_scored=False, key=NoteKind.NORM_HEAD_RELEASE
)
FakeCriticalHeadReleaseNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_HEAD_RELEASE_NOTE, is_scored=False, key=NoteKind.CRIT_HEAD_RELEASE
)
FakeNormalTailTapNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TAIL_TAP_NOTE, is_scored=False, key=NoteKind.NORM_TAIL_TAP
)
FakeCriticalTailTapNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TAIL_TAP_NOTE, is_scored=False, key=NoteKind.CRIT_TAIL_TAP
)
FakeNormalTailFlickNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TAIL_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_TAIL_FLICK
)
FakeCriticalTailFlickNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TAIL_FLICK_NOTE, is_scored=False, key=NoteKind.CRIT_TAIL_FLICK
)
FakeNormalTailTraceNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TAIL_TRACE_NOTE, is_scored=False, key=NoteKind.NORM_TAIL_TRACE
)
FakeCriticalTailTraceNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TAIL_TRACE_NOTE, is_scored=False, key=NoteKind.CRIT_TAIL_TRACE
)
FakeNormalTailTraceFlickNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TAIL_TRACE_FLICK_NOTE, is_scored=False, key=NoteKind.NORM_TAIL_TRACE_FLICK
)
FakeCriticalTailTraceFlickNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TAIL_TRACE_FLICK_NOTE, is_scored=False, key=NoteKind.CRIT_TAIL_TRACE_FLICK
)
FakeNormalTailReleaseNote = BaseNote.derive(
    archetype_names.FAKE_NORMAL_TAIL_RELEASE_NOTE, is_scored=False, key=NoteKind.NORM_TAIL_RELEASE
)
FakeCriticalTailReleaseNote = BaseNote.derive(
    archetype_names.FAKE_CRITICAL_TAIL_RELEASE_NOTE, is_scored=False, key=NoteKind.CRIT_TAIL_RELEASE
)
FakeNormalTickNote = BaseNote.derive(archetype_names.FAKE_NORMAL_TICK_NOTE, is_scored=False, key=NoteKind.NORM_TICK)
FakeCriticalTickNote = BaseNote.derive(archetype_names.FAKE_CRITICAL_TICK_NOTE, is_scored=False, key=NoteKind.CRIT_TICK)
FakeDamageNote = BaseNote.derive(archetype_names.FAKE_DAMAGE_NOTE, is_scored=False, key=NoteKind.DAMAGE)
FakeAnchorNote = BaseNote.derive(archetype_names.FAKE_ANCHOR_NOTE, is_scored=False, key=NoteKind.ANCHOR)
FakeTransientHiddenTickNote = BaseNote.derive(
    archetype_names.FAKE_TRANSIENT_HIDDEN_TICK_NOTE, is_scored=False, key=NoteKind.HIDE_TICK
)


NOTE_ARCHETYPES = (
    NormalTapNote,
    CriticalTapNote,
    NormalFlickNote,
    CriticalFlickNote,
    NormalTraceNote,
    CriticalTraceNote,
    NormalTraceFlickNote,
    CriticalTraceFlickNote,
    NormalReleaseNote,
    CriticalReleaseNote,
    NormalHeadTapNote,
    CriticalHeadTapNote,
    NormalHeadFlickNote,
    CriticalHeadFlickNote,
    NormalHeadTraceNote,
    CriticalHeadTraceNote,
    NormalHeadTraceFlickNote,
    CriticalHeadTraceFlickNote,
    NormalHeadReleaseNote,
    CriticalHeadReleaseNote,
    NormalTailTapNote,
    CriticalTailTapNote,
    NormalTailFlickNote,
    CriticalTailFlickNote,
    NormalTailTraceNote,
    CriticalTailTraceNote,
    NormalTailTraceFlickNote,
    CriticalTailTraceFlickNote,
    NormalTailReleaseNote,
    CriticalTailReleaseNote,
    NormalTickNote,
    CriticalTickNote,
    DamageNote,
    AnchorNote,
    TransientHiddenTickNote,
    FakeNormalTapNote,
    FakeCriticalTapNote,
    FakeNormalFlickNote,
    FakeCriticalFlickNote,
    FakeNormalTraceNote,
    FakeCriticalTraceNote,
    FakeNormalTraceFlickNote,
    FakeCriticalTraceFlickNote,
    FakeNormalReleaseNote,
    FakeCriticalReleaseNote,
    FakeNormalHeadTapNote,
    FakeCriticalHeadTapNote,
    FakeNormalHeadFlickNote,
    FakeCriticalHeadFlickNote,
    FakeNormalHeadTraceNote,
    FakeCriticalHeadTraceNote,
    FakeNormalHeadTraceFlickNote,
    FakeCriticalHeadTraceFlickNote,
    FakeNormalHeadReleaseNote,
    FakeCriticalHeadReleaseNote,
    FakeNormalTailTapNote,
    FakeCriticalTailTapNote,
    FakeNormalTailFlickNote,
    FakeCriticalTailFlickNote,
    FakeNormalTailTraceNote,
    FakeCriticalTailTraceNote,
    FakeNormalTailTraceFlickNote,
    FakeCriticalTailTraceFlickNote,
    FakeNormalTailReleaseNote,
    FakeCriticalTailReleaseNote,
    FakeNormalTickNote,
    FakeCriticalTickNote,
    FakeDamageNote,
    FakeAnchorNote,
    FakeTransientHiddenTickNote,
)


def derive_note_archetypes[T: type[AnyArchetype]](base: T) -> tuple[T, ...]:
    """Helper function to derive all note archetypes from a given base archetype for used in watch and preview."""
    return tuple(base.derive(str(a.name), is_scored=a.is_scored, key=a.key) for a in NOTE_ARCHETYPES)
