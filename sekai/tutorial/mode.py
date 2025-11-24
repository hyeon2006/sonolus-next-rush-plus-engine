from sonolus.script.engine import TutorialMode

from sekai.lib.effect import Effects
from sekai.lib.particle import Particles
from sekai.lib.skin import Skin
from sekai.tutorial.instructions import InstructionIcons, Instructions
from sekai.tutorial.navigate import navigate
from sekai.tutorial.preprocess import preprocess
from sekai.tutorial.update import update

tutorial_mode = TutorialMode(
    skin=Skin,
    effects=Effects,
    particles=Particles,
    instructions=Instructions,
    instruction_icons=InstructionIcons,
    preprocess=preprocess,
    navigate=navigate,
    update=update,
)
