from sonolus.script.engine import PlayMode

from sekai.lib.buckets import Buckets
from sekai.lib.effect import Effects
from sekai.lib.particle import Particles
from sekai.lib.skin import BaseSkin
from sekai.play.bpm_change import BpmChange
from sekai.play.connector import CONNECTOR_ARCHETYPES
from sekai.play.initialization import Initialization
from sekai.play.input_manager import InputManager
from sekai.play.note import NOTE_ARCHETYPES
from sekai.play.sim_line import SimLine
from sekai.play.slot_effect import SLOT_EFFECT_ARCHETYPES
from sekai.play.stage import Stage
from sekai.play.timescale import TimescaleChange, TimescaleGroup

play_mode = PlayMode(
    archetypes=[
        Initialization,
        Stage,
        InputManager,
        BpmChange,
        TimescaleGroup,
        TimescaleChange,
        *NOTE_ARCHETYPES,
        *CONNECTOR_ARCHETYPES,
        *SLOT_EFFECT_ARCHETYPES,
        SimLine,
    ],
    skin=BaseSkin,
    effects=Effects,
    particles=Particles,
    buckets=Buckets,
)
