from sonolus.script.globals import level_memory


@level_memory
class PlayLevelMemory:
    last_note_sfx_time: float


def init_play_common():
    PlayLevelMemory.last_note_sfx_time = -1e8
