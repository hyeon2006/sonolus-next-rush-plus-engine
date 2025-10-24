from sonolus.script.particle import Particle, StandardParticle, particle, particles
from sonolus.script.record import Record

EMPTY_PARTICLE = Particle(-1)


@particles
class Particles:
    lane: StandardParticle.LANE_LINEAR

    normal_note_lane_linear: Particle = particle("Sekai Note Lane Linear")
    normal_flick_note_lane_linear: Particle = particle("Sekai Note Lane Linear")
    critical_note_lane_linear: Particle = particle("Sekai Critical Lane Linear")
    critical_flick_note_lane_linear: Particle = particle("Sekai Critical Flick Lane Linear")

    normal_note_circular: StandardParticle.NOTE_CIRCULAR_TAP_CYAN
    normal_note_linear: StandardParticle.NOTE_LINEAR_TAP_CYAN
    normal_note_slot_linear: Particle = particle("Sekai Slot Linear Tap Cyan")

    slide_note_circular: StandardParticle.NOTE_CIRCULAR_TAP_GREEN
    slide_note_linear: StandardParticle.NOTE_LINEAR_TAP_GREEN
    slide_note_slot_linear: Particle = particle("Sekai Slot Linear Slide Tap Green")

    flick_note_circular: StandardParticle.NOTE_CIRCULAR_TAP_RED
    flick_note_linear: StandardParticle.NOTE_LINEAR_TAP_RED
    flick_note_slot_linear: Particle = particle("Sekai Slot Linear Alternative Red")

    flick_note_directional: StandardParticle.NOTE_LINEAR_ALTERNATIVE_RED

    trace_note_circular: Particle = particle("Sekai Trace Note Circular Green")
    trace_note_linear: Particle = particle("Sekai Trace Note Linear Green")

    critical_note_circular: StandardParticle.NOTE_CIRCULAR_TAP_YELLOW
    critical_note_linear: StandardParticle.NOTE_LINEAR_TAP_YELLOW
    critical_note_slot_linear: Particle = particle("Sekai Slot Linear Tap Yellow")

    critical_slide_note_circular: Particle = particle("Sekai Critical Slide Circular Yellow")
    critical_slide_note_linear: Particle = particle("Sekai Critical Slide Linear Yellow")
    critical_slide_note_slot_linear: Particle = particle("Sekai Slot Linear Slide Tap Yellow")

    critical_flick_note_circular: Particle = particle("Sekai Critical Flick Circular Yellow")
    critical_flick_note_linear: Particle = particle("Sekai Critical Flick Linear Yellow")
    critical_flick_note_slot_linear: Particle = particle("Sekai Slot Linear Alternative Yellow")

    critical_note_directional: StandardParticle.NOTE_LINEAR_ALTERNATIVE_YELLOW

    critical_trace_note_circular: Particle = particle("Sekai Trace Note Circular Yellow")
    critical_trace_note_linear: Particle = particle("Sekai Trace Note Linear Yellow")

    normal_slide_tick_note: StandardParticle.NOTE_CIRCULAR_ALTERNATIVE_GREEN

    critical_slide_tick_note: StandardParticle.NOTE_CIRCULAR_ALTERNATIVE_YELLOW

    normal_slide_connector_circular: StandardParticle.NOTE_CIRCULAR_HOLD_GREEN
    normal_slide_connector_linear: StandardParticle.NOTE_LINEAR_HOLD_GREEN
    normal_slide_connector_trail_linear: Particle = particle("Sekai Normal Slide Trail Linear")
    normal_slide_connector_slot_linear: Particle = particle("Sekai Slot Linear Slide Green")

    critical_slide_connector_circular: StandardParticle.NOTE_CIRCULAR_HOLD_YELLOW
    critical_slide_connector_linear: StandardParticle.NOTE_LINEAR_HOLD_YELLOW
    critical_slide_connector_trail_linear: Particle = particle("Sekai Critical Slide Trail Linear")
    critical_slide_connector_slot_linear: Particle = particle("Sekai Slot Linear Slide Yellow")

    damage_note_circular: StandardParticle.NOTE_CIRCULAR_TAP_PURPLE
    damage_note_linear: StandardParticle.NOTE_LINEAR_TAP_PURPLE


class NoteParticleSet(Record):
    circular: Particle
    circular_fallback: Particle
    linear: Particle
    linear_fallback: Particle
    directional: Particle
    tick: Particle
    lane: Particle
    lane_basic: Particle
    slot_linear: Particle


normal_note_particles = NoteParticleSet(
    circular=Particles.normal_note_circular,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.normal_note_linear,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=Particles.normal_note_lane_linear,
    lane_basic=Particles.lane,
    slot_linear=Particles.normal_note_slot_linear,
)
slide_note_particles = NoteParticleSet(
    circular=Particles.slide_note_circular,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.slide_note_linear,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=Particles.normal_note_lane_linear,
    lane_basic=Particles.lane,
    slot_linear=Particles.slide_note_slot_linear,
)
flick_note_particles = NoteParticleSet(
    circular=Particles.flick_note_circular,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.flick_note_linear,
    directional=Particles.flick_note_directional,
    linear_fallback=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=Particles.flick_note_slot_linear,
)
trace_note_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.trace_note_linear,
    linear_fallback=Particles.slide_note_linear,
    directional=EMPTY_PARTICLE,
    tick=Particles.trace_note_circular,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
trace_flick_note_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=EMPTY_PARTICLE,
    directional=Particles.flick_note_directional,
    linear_fallback=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
critical_note_particles = NoteParticleSet(
    circular=Particles.critical_note_circular,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.critical_note_linear,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=Particles.critical_note_lane_linear,
    lane_basic=Particles.lane,
    slot_linear=Particles.critical_note_slot_linear,
)
critical_slide_note_particles = NoteParticleSet(
    circular=Particles.critical_slide_note_circular,
    circular_fallback=Particles.critical_note_circular,
    linear=Particles.critical_slide_note_linear,
    linear_fallback=Particles.critical_note_linear,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=Particles.critical_note_lane_linear,
    lane_basic=Particles.lane,
    slot_linear=Particles.critical_slide_note_slot_linear,
)
critical_flick_note_particles = NoteParticleSet(
    circular=Particles.critical_flick_note_circular,
    circular_fallback=Particles.critical_note_circular,
    linear=Particles.critical_flick_note_linear,
    linear_fallback=Particles.critical_note_linear,
    directional=Particles.critical_note_directional,
    tick=EMPTY_PARTICLE,
    lane=Particles.critical_flick_note_lane_linear,
    lane_basic=Particles.lane,
    slot_linear=Particles.critical_flick_note_slot_linear,
)
critical_trace_note_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.critical_trace_note_linear,
    linear_fallback=Particles.critical_note_linear,
    directional=EMPTY_PARTICLE,
    tick=Particles.critical_trace_note_circular,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
critical_trace_flick_note_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=EMPTY_PARTICLE,
    linear_fallback=EMPTY_PARTICLE,
    directional=Particles.critical_note_directional,
    tick=EMPTY_PARTICLE,
    lane=Particles.critical_flick_note_lane_linear,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
damage_note_particles = NoteParticleSet(
    circular=Particles.damage_note_circular,
    circular_fallback=EMPTY_PARTICLE,
    linear=Particles.damage_note_linear,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
normal_tick_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=EMPTY_PARTICLE,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=Particles.normal_slide_tick_note,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
critical_tick_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=EMPTY_PARTICLE,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=Particles.critical_slide_tick_note,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)
empty_note_particles = NoteParticleSet(
    circular=EMPTY_PARTICLE,
    circular_fallback=EMPTY_PARTICLE,
    linear=EMPTY_PARTICLE,
    linear_fallback=EMPTY_PARTICLE,
    directional=EMPTY_PARTICLE,
    tick=EMPTY_PARTICLE,
    lane=EMPTY_PARTICLE,
    lane_basic=EMPTY_PARTICLE,
    slot_linear=EMPTY_PARTICLE,
)


def first_available_particle(*args: Particle) -> Particle:
    result = +EMPTY_PARTICLE
    for e in args:
        if e.is_available:
            result @= e
            break
    return result
