from sonolus.script.globals import level_data
from sonolus.script.particle import Particle, StandardParticle, particle, particles
from sonolus.script.record import Record


@particles
class BaseParticles:
    lane: StandardParticle.LANE_LINEAR

    normal_note_lane_linear: Particle = particle("Sekai Note Lane Linear")
    normal_slide_note_lane_linear: Particle = particle("Sekai Slide Lane Linear")
    normal_flick_note_lane_linear: Particle = particle("Sekai Flick Lane Linear")
    normal_down_flick_note_lane_linear: Particle = particle("Sekai Down Flick Lane Linear")
    critical_note_lane_linear: Particle = particle("Sekai Critical Lane Linear")
    critical_slide_note_lane_linear: Particle = particle("Sekai Critical Slide Lane Linear")
    critical_flick_note_lane_linear: Particle = particle("Sekai Critical Flick Lane Linear")
    critical_down_flick_note_lane_linear: Particle = particle("Sekai Critical Down Flick Lane Linear")

    note_circular_cyan: StandardParticle.NOTE_CIRCULAR_TAP_CYAN
    note_linear_cyan: StandardParticle.NOTE_LINEAR_TAP_CYAN
    note_slot_linear_cyan: Particle = particle("Sekai Slot Linear Tap Cyan")

    note_circular_green: StandardParticle.NOTE_CIRCULAR_TAP_GREEN
    note_linear_green: StandardParticle.NOTE_LINEAR_TAP_GREEN
    note_slot_linear_green: Particle = particle("Sekai Slot Linear Tap Green")

    note_circular_red: StandardParticle.NOTE_CIRCULAR_TAP_RED
    note_linear_red: StandardParticle.NOTE_LINEAR_TAP_RED
    note_slot_linear_alternative_red: Particle = particle("Sekai Slot Linear Alternative Red")
    note_directional_red: StandardParticle.NOTE_LINEAR_ALTERNATIVE_RED

    trace_note_circular_green: Particle = particle("Sekai Trace Note Circular Green")
    trace_note_linear_green: Particle = particle("Sekai Trace Note Linear Green")

    note_circular_yellow: StandardParticle.NOTE_CIRCULAR_TAP_YELLOW
    note_linear_yellow: StandardParticle.NOTE_LINEAR_TAP_YELLOW
    note_slot_linear_yellow: Particle = particle("Sekai Slot Linear Tap Yellow")

    note_circular_slide_yellow: Particle = particle("Sekai Critical Slide Circular Yellow")
    note_linear_slide_yellow: Particle = particle("Sekai Critical Slide Linear Yellow")
    note_slot_linear_slide_yellow: Particle = particle("Sekai Slot Linear Slide Tap Yellow")

    note_circular_flick_yellow: Particle = particle("Sekai Critical Flick Circular Yellow")
    note_linear_flick_yellow: Particle = particle("Sekai Critical Flick Linear Yellow")
    note_slot_linear_flick_yellow: Particle = particle("Sekai Slot Linear Alternative Yellow")
    note_directional_yellow: StandardParticle.NOTE_LINEAR_ALTERNATIVE_YELLOW

    trace_note_circular_yellow: Particle = particle("Sekai Trace Note Circular Yellow")
    trace_note_linear_yellow: Particle = particle("Sekai Trace Note Linear Yellow")

    slide_tick_note_circular_green: StandardParticle.NOTE_CIRCULAR_ALTERNATIVE_GREEN

    slide_tick_note_circular_yellow: StandardParticle.NOTE_CIRCULAR_ALTERNATIVE_YELLOW

    slide_connector_circular_green: StandardParticle.NOTE_CIRCULAR_HOLD_GREEN
    slide_connector_linear_green: StandardParticle.NOTE_LINEAR_HOLD_GREEN
    slide_connector_trail_linear_green: Particle = particle("Sekai Normal Slide Trail Linear")
    slide_connector_slot_linear_green: Particle = particle("Sekai Slot Linear Slide Green")

    slide_connector_circular_yellow: StandardParticle.NOTE_CIRCULAR_HOLD_YELLOW
    slide_connector_linear_yellow: StandardParticle.NOTE_LINEAR_HOLD_YELLOW
    slide_connector_trail_linear_yellow: Particle = particle("Sekai Critical Slide Trail Linear")
    slide_connector_slot_linear_yellow: Particle = particle("Sekai Slot Linear Slide Yellow")

    note_circular_purple: StandardParticle.NOTE_CIRCULAR_TAP_PURPLE
    note_linear_purple: StandardParticle.NOTE_LINEAR_TAP_PURPLE

    normal_note_circular: Particle = particle("Sekai Normal Note Circular")
    normal_note_linear: Particle = particle("Sekai Normal Note Linear")
    normal_note_slot_linear: Particle = particle("Sekai Normal Note Slot Linear")

    slide_note_circular: Particle = particle("Sekai Slide Note Circular")
    slide_note_linear: Particle = particle("Sekai Slide Note Linear")
    slide_note_slot_linear: Particle = particle("Sekai Slide Note Slot Linear")

    flick_note_circular: Particle = particle("Sekai Flick Note Circular")
    flick_note_linear: Particle = particle("Sekai Flick Note Linear")
    flick_note_slot_linear: Particle = particle("Sekai Flick Note Slot Linear")

    flick_note_directional: Particle = particle("Sekai Flick Note Directional")

    down_flick_note_circular: Particle = particle("Sekai Down Flick Note Circular")
    down_flick_note_linear: Particle = particle("Sekai Down Flick Note Linear")
    down_flick_note_slot_linear: Particle = particle("Sekai Down Flick Note Slot Linear")

    down_flick_note_directional: Particle = particle("Sekai Down Flick Note Directional")

    trace_note_circular: Particle = particle("Sekai Trace Note Circular")
    trace_note_linear: Particle = particle("Sekai Trace Note Linear")

    critical_note_circular: Particle = particle("Sekai Critical Note Circular")
    critical_note_linear: Particle = particle("Sekai Critical Note Linear")
    critical_note_slot_linear: Particle = particle("Sekai Critical Note Slot Linear")

    critical_slide_note_circular: Particle = particle("Sekai Critical Slide Note Circular")
    critical_slide_note_linear: Particle = particle("Sekai Critical Slide Note Linear")
    critical_slide_note_slot_linear: Particle = particle("Sekai Critical Slide Note Slot Linear")

    critical_flick_note_circular: Particle = particle("Sekai Critical Flick Note Circular")
    critical_flick_note_linear: Particle = particle("Sekai Critical Flick Note Linear")
    critical_flick_note_slot_linear: Particle = particle("Sekai Critical Flick Note Slot Linear")

    critical_note_directional: Particle = particle("Sekai Critical Note Directional")

    critical_down_flick_note_circular: Particle = particle("Sekai Critical Down Flick Note Circular")
    critical_down_flick_note_linear: Particle = particle("Sekai Critical Down Flick Note Linear")
    critical_down_flick_note_slot_linear: Particle = particle("Sekai Critical Down Flick Note Slot Linear")

    critical_down_flick_note_directional: Particle = particle("Sekai Critical Down Flick Note Directional")

    critical_trace_note_circular: Particle = particle("Sekai Critical Trace Note Circular")
    critical_trace_note_linear: Particle = particle("Sekai Critical Trace Note Linear")

    normal_slide_tick_note: Particle = particle("Sekai Normal Slide Tick Note")

    critical_slide_tick_note: Particle = particle("Sekai Critical Slide Tick Note")

    normal_slide_connector_circular: Particle = particle("Sekai Normal Slide Connector Circular")
    normal_slide_connector_linear: Particle = particle("Sekai Normal Slide Connector Linear")
    normal_slide_connector_trail_linear: Particle = particle("Sekai Normal Slide Connector Trail Linear")
    normal_slide_connector_slot_linear: Particle = particle("Sekai Normal Slide Connector Slot Linear")

    critical_slide_connector_circular: Particle = particle("Sekai Critical Slide Connector Circular")
    critical_slide_connector_linear: Particle = particle("Sekai Critical Slide Connector Linear")
    critical_slide_connector_trail_linear: Particle = particle("Sekai Critical Slide Connector Trail Linear")
    critical_slide_connector_slot_linear: Particle = particle("Sekai Critical Slide Connector Slot Linear")

    damage_note_circular: Particle = particle("Sekai Damage Note Circular")
    damage_note_linear: Particle = particle("Sekai Damage Note Linear")


EMPTY_PARTICLE = Particle(-1)


class NoteParticleSet(Record):
    circular: Particle
    linear: Particle
    directional: Particle
    tick: Particle
    lane: Particle
    lane_basic: Particle
    slot_linear: Particle


EMPTY_NOTE_PARTICLE_SET = NoteParticleSet(
    circular=EMPTY_PARTICLE,
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


class ActiveConnectorParticleSet(Record):
    circular: Particle
    linear: Particle
    trail_linear: Particle
    slot_linear: Particle


def first_available_particle(*args: Particle) -> Particle:
    result = +EMPTY_PARTICLE
    for e in args:
        if e.is_available:
            result @= e
            break
    return result


@level_data
class ActiveParticles:
    lane: Particle

    normal_note: NoteParticleSet
    slide_note: NoteParticleSet
    flick_note: NoteParticleSet
    down_flick_note: NoteParticleSet
    critical_note: NoteParticleSet
    critical_slide_note: NoteParticleSet
    critical_flick_note: NoteParticleSet
    critical_down_flick_note: NoteParticleSet
    trace_note: NoteParticleSet
    trace_flick_note: NoteParticleSet
    trace_down_flick_note: NoteParticleSet
    critical_trace_note: NoteParticleSet
    critical_trace_flick_note: NoteParticleSet
    critical_trace_down_flick_note: NoteParticleSet
    normal_slide_tick_note: NoteParticleSet
    critical_slide_tick_note: NoteParticleSet
    damage_note: NoteParticleSet

    normal_slide_connector: ActiveConnectorParticleSet
    critical_slide_connector: ActiveConnectorParticleSet


def init_particles():
    ActiveParticles.lane @= BaseParticles.lane

    ActiveParticles.normal_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.normal_note_circular,
            BaseParticles.note_circular_cyan,
        ),
        linear=first_available_particle(
            BaseParticles.normal_note_linear,
            BaseParticles.note_linear_cyan,
        ),
        directional=EMPTY_PARTICLE,
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.normal_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.normal_note_slot_linear,
            BaseParticles.note_slot_linear_cyan,
        ),
    )
    ActiveParticles.slide_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.slide_note_circular,
            BaseParticles.note_circular_green,
        ),
        linear=first_available_particle(
            BaseParticles.slide_note_linear,
            BaseParticles.note_linear_green,
        ),
        directional=EMPTY_PARTICLE,
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.normal_slide_note_lane_linear,
            BaseParticles.normal_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.slide_note_slot_linear,
            BaseParticles.note_slot_linear_green,
        ),
    )
    ActiveParticles.flick_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.flick_note_circular,
            BaseParticles.note_circular_red,
        ),
        linear=first_available_particle(
            BaseParticles.flick_note_linear,
            BaseParticles.note_linear_red,
        ),
        directional=first_available_particle(
            BaseParticles.flick_note_directional,
            BaseParticles.note_directional_red,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            # Disabled unless explicitly set, so no fallback
            BaseParticles.normal_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=first_available_particle(
            BaseParticles.flick_note_slot_linear,
            BaseParticles.note_slot_linear_alternative_red,
        ),
    )
    ActiveParticles.down_flick_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.down_flick_note_circular,
            BaseParticles.flick_note_circular,
            BaseParticles.note_circular_red,
        ),
        linear=first_available_particle(
            BaseParticles.down_flick_note_linear,
            BaseParticles.flick_note_linear,
            BaseParticles.note_linear_red,
        ),
        directional=first_available_particle(
            BaseParticles.down_flick_note_directional,
            BaseParticles.flick_note_directional,
            BaseParticles.note_directional_red,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.normal_down_flick_note_lane_linear,
            BaseParticles.normal_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=first_available_particle(
            BaseParticles.down_flick_note_slot_linear,
            BaseParticles.flick_note_slot_linear,
            BaseParticles.note_slot_linear_alternative_red,
        ),
    )
    ActiveParticles.critical_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.critical_note_circular,
            BaseParticles.note_circular_yellow,
        ),
        linear=first_available_particle(
            BaseParticles.critical_note_linear,
            BaseParticles.note_linear_yellow,
        ),
        directional=EMPTY_PARTICLE,
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.critical_note_slot_linear,
            BaseParticles.note_slot_linear_yellow,
        ),
    )
    ActiveParticles.critical_slide_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.critical_slide_note_circular,
            BaseParticles.note_circular_slide_yellow,
            BaseParticles.critical_note_circular,
            BaseParticles.note_circular_yellow,
        ),
        linear=first_available_particle(
            BaseParticles.critical_slide_note_linear,
            BaseParticles.note_linear_slide_yellow,
            BaseParticles.critical_note_linear,
            BaseParticles.note_linear_yellow,
        ),
        directional=EMPTY_PARTICLE,
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_slide_note_lane_linear,
            BaseParticles.critical_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.critical_slide_note_slot_linear,
            BaseParticles.note_slot_linear_slide_yellow,
            BaseParticles.critical_note_slot_linear,
            BaseParticles.note_slot_linear_yellow,
        ),
    )
    ActiveParticles.critical_flick_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.critical_flick_note_circular,
            BaseParticles.note_circular_flick_yellow,
            BaseParticles.critical_note_circular,
            BaseParticles.note_circular_yellow,
        ),
        linear=first_available_particle(
            BaseParticles.critical_flick_note_linear,
            BaseParticles.note_linear_flick_yellow,
            BaseParticles.critical_note_linear,
            BaseParticles.note_linear_yellow,
        ),
        directional=first_available_particle(
            BaseParticles.critical_note_directional,
            BaseParticles.note_directional_yellow,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_flick_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.critical_flick_note_slot_linear,
            BaseParticles.note_slot_linear_flick_yellow,
            BaseParticles.critical_note_slot_linear,
            BaseParticles.note_slot_linear_yellow,
        ),
    )
    ActiveParticles.critical_down_flick_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.critical_down_flick_note_circular,
            BaseParticles.critical_flick_note_circular,
            BaseParticles.note_circular_flick_yellow,
            BaseParticles.critical_note_circular,
            BaseParticles.note_circular_yellow,
        ),
        linear=first_available_particle(
            BaseParticles.critical_down_flick_note_linear,
            BaseParticles.critical_flick_note_linear,
            BaseParticles.note_linear_flick_yellow,
            BaseParticles.critical_note_linear,
            BaseParticles.note_linear_yellow,
        ),
        directional=first_available_particle(
            BaseParticles.critical_down_flick_note_directional,
            BaseParticles.critical_note_directional,
            BaseParticles.note_directional_yellow,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_down_flick_note_lane_linear,
            BaseParticles.critical_flick_note_lane_linear,
        ),
        lane_basic=BaseParticles.lane,
        slot_linear=first_available_particle(
            BaseParticles.critical_down_flick_note_slot_linear,
            BaseParticles.critical_flick_note_slot_linear,
            BaseParticles.note_slot_linear_flick_yellow,
            BaseParticles.critical_note_slot_linear,
            BaseParticles.note_slot_linear_yellow,
        ),
    )
    ActiveParticles.trace_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=first_available_particle(
            BaseParticles.trace_note_linear,
            BaseParticles.trace_note_linear_green,
        ),
        directional=EMPTY_PARTICLE,
        tick=first_available_particle(
            BaseParticles.trace_note_circular,
            BaseParticles.trace_note_circular_green,
        ),
        lane=EMPTY_PARTICLE,
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.trace_flick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=first_available_particle(
            BaseParticles.flick_note_directional,
            BaseParticles.note_directional_red,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.normal_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.trace_down_flick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=first_available_particle(
            BaseParticles.down_flick_note_directional,
            BaseParticles.flick_note_directional,
            BaseParticles.note_directional_red,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.normal_down_flick_note_lane_linear,
            BaseParticles.normal_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.critical_trace_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=first_available_particle(
            BaseParticles.critical_trace_note_linear,
            BaseParticles.trace_note_linear_yellow,
        ),
        directional=EMPTY_PARTICLE,
        tick=first_available_particle(
            BaseParticles.critical_trace_note_circular,
            BaseParticles.trace_note_circular_yellow,
        ),
        lane=EMPTY_PARTICLE,
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.critical_trace_flick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=first_available_particle(
            BaseParticles.critical_note_directional,
            BaseParticles.note_directional_yellow,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.critical_trace_down_flick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=first_available_particle(
            BaseParticles.critical_down_flick_note_directional,
            BaseParticles.critical_note_directional,
            BaseParticles.note_directional_yellow,
        ),
        tick=EMPTY_PARTICLE,
        lane=first_available_particle(
            BaseParticles.critical_down_flick_note_lane_linear,
            BaseParticles.critical_flick_note_lane_linear,
        ),
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.normal_slide_tick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=EMPTY_PARTICLE,
        tick=first_available_particle(
            BaseParticles.normal_slide_tick_note,
            BaseParticles.slide_tick_note_circular_green,
        ),
        lane=EMPTY_PARTICLE,
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.critical_slide_tick_note @= NoteParticleSet(
        circular=EMPTY_PARTICLE,
        linear=EMPTY_PARTICLE,
        directional=EMPTY_PARTICLE,
        tick=first_available_particle(
            BaseParticles.critical_slide_tick_note,
            BaseParticles.slide_tick_note_circular_yellow,
        ),
        lane=EMPTY_PARTICLE,
        lane_basic=EMPTY_PARTICLE,
        slot_linear=EMPTY_PARTICLE,
    )
    ActiveParticles.damage_note @= NoteParticleSet(
        circular=first_available_particle(
            BaseParticles.damage_note_circular,
        ),
        linear=first_available_particle(
            BaseParticles.damage_note_linear,
        ),
        directional=EMPTY_PARTICLE,
        tick=EMPTY_PARTICLE,
        lane=EMPTY_PARTICLE,
        lane_basic=BaseParticles.lane,
        slot_linear=EMPTY_PARTICLE,
    )

    ActiveParticles.normal_slide_connector @= ActiveConnectorParticleSet(
        circular=first_available_particle(
            BaseParticles.normal_slide_connector_circular,
            BaseParticles.slide_connector_circular_green,
        ),
        linear=first_available_particle(
            BaseParticles.normal_slide_connector_linear,
            BaseParticles.slide_connector_linear_green,
        ),
        trail_linear=first_available_particle(
            BaseParticles.normal_slide_connector_trail_linear,
            BaseParticles.slide_connector_trail_linear_green,
        ),
        slot_linear=first_available_particle(
            BaseParticles.normal_slide_connector_slot_linear,
            BaseParticles.slide_connector_slot_linear_green,
        ),
    )
    ActiveParticles.critical_slide_connector @= ActiveConnectorParticleSet(
        circular=first_available_particle(
            BaseParticles.critical_slide_connector_circular,
            BaseParticles.slide_connector_circular_yellow,
        ),
        linear=first_available_particle(
            BaseParticles.critical_slide_connector_linear,
            BaseParticles.slide_connector_linear_yellow,
        ),
        trail_linear=first_available_particle(
            BaseParticles.critical_slide_connector_trail_linear,
            BaseParticles.slide_connector_trail_linear_yellow,
        ),
        slot_linear=first_available_particle(
            BaseParticles.critical_slide_connector_slot_linear, BaseParticles.slide_connector_slot_linear_yellow
        ),
    )
