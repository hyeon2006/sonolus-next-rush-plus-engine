from math import ceil

from sonolus.script.archetype import EntityRef, PreviewArchetype, callback, imported
from sonolus.script.printing import PrintColor, PrintFormat
from sonolus.script.quad import Quad
from sonolus.script.timing import beat_to_time

from sekai.lib import archetype_names
from sekai.lib.baseevent import init_event_list
from sekai.lib.layer import LAYER_BEAT_LINE, get_z
from sekai.lib.layout import get_camera_info
from sekai.lib.level_config import EngineRevision, LevelConfig, init_level_config
from sekai.lib.particle import init_particles
from sekai.lib.skin import ActiveSkin, init_skin
from sekai.lib.ui import init_ui
from sekai.preview.dynamic_stage import PreviewCameraChange
from sekai.preview.layout import (
    PREVIEW_CAMERA_INTERVAL,
    PREVIEW_CAMERA_MARKER_ALPHA,
    PREVIEW_COLUMN_SECS,
    PreviewData,
    PreviewLayout,
    init_preview_layout,
    layout_preview_bar_line,
    layout_preview_camera_marker,
    layout_preview_column_divider,
    print_at_col_top,
)
from sekai.preview.stage import draw_preview_cover, draw_preview_stage


class PreviewInitialization(PreviewArchetype):
    name = archetype_names.INITIALIZATION

    revision: EngineRevision = imported(name="revision", default=EngineRevision.LATEST)
    first_camera_ref: EntityRef[PreviewCameraChange] = imported(name="firstCamera")

    @callback(order=1)
    def preprocess(self):
        if not ActiveSkin.lane_background_preview.is_available:
            LevelConfig.dynamic_stages = False

        init_level_config(self.revision)
        init_ui()
        init_skin()
        init_particles()
        init_preview_layout()
        init_event_list(self.first_camera_ref)

    def render(self):
        if not LevelConfig.dynamic_stages:
            draw_preview_stage()
        draw_preview_cover()
        print_preview_col_head_text()
        draw_beat_lines()
        if LevelConfig.dynamic_stages:
            draw_column_dividers()
            draw_camera_markers()


def print_preview_col_head_text():
    combo = 0
    for col in range(PreviewLayout.column_count):
        if col < len(PreviewData.note_counts_by_col):
            combo += PreviewData.note_counts_by_col[col]
            print_at_col_top(combo, col, fmt=PrintFormat.ENTITY_COUNT, color=PrintColor.RED, side="right")
        print_at_col_top((col + 1) * PREVIEW_COLUMN_SECS, col, fmt=PrintFormat.TIME, color=PrintColor.CYAN, side="left")


def draw_beat_lines():
    for beat in range(int(PreviewData.max_beat) + 1):
        for beat_offset, extend_scale in (
            (0, 0.3),
            (0.25, 0.1),
            (0.5, 0.2),
            (0.75, 0.1),
        ):
            t = beat_to_time(beat + beat_offset)
            left_layout = +Quad
            right_layout = +Quad
            if LevelConfig.dynamic_stages:
                left_layout @= layout_preview_bar_line(t, extend="left_in", extend_scale=extend_scale)
                right_layout @= layout_preview_bar_line(t, extend="right_in", extend_scale=extend_scale)
            else:
                left_layout @= layout_preview_bar_line(t, extend="left_only", extend_scale=extend_scale)
                right_layout @= layout_preview_bar_line(t, extend="right_only", extend_scale=extend_scale)
            ActiveSkin.beat_line.draw(left_layout, z=get_z(LAYER_BEAT_LINE), a=0.5)
            ActiveSkin.beat_line.draw(right_layout, z=get_z(LAYER_BEAT_LINE), a=0.5)


def draw_column_dividers():
    for col in range(1, PreviewLayout.column_count):
        ActiveSkin.preview_divider.draw(layout_preview_column_divider(col), z=get_z(LAYER_BEAT_LINE), a=0.5)


def draw_camera_markers():
    count = int(ceil(PreviewData.max_time / PREVIEW_COLUMN_SECS) * PREVIEW_COLUMN_SECS / PREVIEW_CAMERA_INTERVAL)
    for i in range(count + 1):
        t = (i + 0.5) * PREVIEW_CAMERA_INTERVAL
        camera = get_camera_info(t)
        left_layout = layout_preview_camera_marker(camera.lane - camera.size, t)
        right_layout = layout_preview_camera_marker(camera.lane + camera.size, t)
        ActiveSkin.special_line.draw(left_layout, z=get_z(LAYER_BEAT_LINE), a=PREVIEW_CAMERA_MARKER_ALPHA)
        ActiveSkin.special_line.draw(right_layout, z=get_z(LAYER_BEAT_LINE), a=PREVIEW_CAMERA_MARKER_ALPHA)
