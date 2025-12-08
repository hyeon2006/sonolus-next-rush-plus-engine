from math import cos, floor, log, pi

from sonolus.script.bucket import Judgment, JudgmentWindow
from sonolus.script.interval import Interval, unlerp, unlerp_clamped
from sonolus.script.record import Record
from sonolus.script.runtime import runtime_ui, screen, time
from sonolus.script.vec import Vec2

from sekai.lib.layout import (
    ComboType,
    Layout,
    Quad,
    layout_combo_label,
    transform_quad,
)
from sekai.lib.options import Options
from sekai.lib.skin import (
    ActiveSkin,
)


def transform_fixed_size(h, w):
    target_width = w * Layout.fixed_w_scale
    target_height = h * Layout.fixed_h_scale

    width = target_width / Layout.w_scale
    height = target_height / Layout.h_scale

    return height, width


def draw_combo_label(ap: bool, z: float, glow_z=float):
    ui = runtime_ui()

    screen_center = Vec2(x=5.337, y=0.485)

    base_h = 0.04225 * ui.combo_config.scale
    base_w = base_h * 3.22 * 6.65
    h, w = transform_fixed_size(base_h, base_w)
    a = ui.combo_config.alpha * 0.8 * (cos(time() * pi) + 1) / 2
    layout = layout_combo_label(screen_center, w=w / 2, h=h / 2)
    if ap or not Options.ap_effect:
        ActiveSkin.combo_label.get_sprite(ComboType.NORMAL).draw(quad=layout, z=z, a=ui.combo_config.alpha)
    else:
        ActiveSkin.combo_label.get_sprite(ComboType.AP).draw(quad=layout, z=z, a=ui.combo_config.alpha)
        ActiveSkin.combo_label.get_sprite(ComboType.GLOW).draw(quad=layout, z=glow_z, a=a)


def draw_combo_number(draw_time: float, ap: bool, combo: int, z: float, z2: float, z3: float):
    ui = runtime_ui()

    digit_count = 1 if combo == 0 else floor(log(combo, 10)) + 1  # noqa: FURB163

    screen_center = Vec2(x=5.337, y=0.585)

    base_h = 0.1222 * ui.combo_config.scale
    base_h2 = 0.15886 * ui.combo_config.scale
    base_w = base_h * 0.79 * 7
    base_w2 = base_h2 * 0.79 * 7

    s = 0.6 + 0.4 * unlerp_clamped(draw_time, draw_time + 0.112, time())
    s2 = 0.762 + 0.231 * unlerp_clamped(draw_time + 0.112, draw_time + 0.192, time())

    a = ui.combo_config.alpha
    a2 = (
        ui.combo_config.alpha * unlerp(draw_time + 0.192, draw_time + 0.112, time())
        if time() >= draw_time + 0.112
        else 0
    )
    a3 = ui.combo_config.alpha * 0.8 * (cos(time() * pi) + 1) / 2

    h, w = transform_fixed_size(base_h, base_w)
    h2, w2 = transform_fixed_size(base_h2, base_w2)

    digit_gap = w * Options.combo_distance
    digit_gap2 = w2 * Options.combo_distance
    total_width = digit_count * w + (digit_count - 1) * digit_gap
    total_width2 = digit_count * w2 + (digit_count - 1) * digit_gap2
    start_x = screen_center.x - total_width / 2
    start_x2 = screen_center.x - total_width2 / 2

    drawing_combo = ComboNumberLayout(
        core=CoreConfig(
            ap=ap,
            combo_number=combo,
            digit_count=digit_count,
        ),
        common=CommonConfig(
            center_x=screen_center.x,
            center_y=screen_center.y,
        ),
        alpha=AlphaConfig(
            a=a,
            a2=a2,
            a3=a3,
        ),
        layout1=LayoutConfig(
            width=w,
            gap=digit_gap,
            scale=s,
            height=h,
            start_x=start_x,
        ),
        layout2=LayoutConfig(
            width=w2,
            gap=digit_gap2,
            scale=s2,
            height=h2,
            start_x=start_x2,
        ),
    )
    drawing_combo.draw_number(z=z, z2=z2, z3=z3)


class CoreConfig(Record):
    ap: bool
    combo_number: int
    digit_count: int


class CommonConfig(Record):
    center_x: float
    center_y: float


class AlphaConfig(Record):
    a: float
    a2: float
    a3: float


class LayoutConfig(Record):
    width: float
    gap: float
    scale: float
    height: float
    start_x: float


class ComboNumberLayout(Record):
    core: CoreConfig
    common: CommonConfig
    alpha: AlphaConfig
    layout1: LayoutConfig
    layout2: LayoutConfig

    def layout_combo_number(self, l: float, r: float, t: float, b: float) -> Quad:
        return transform_quad(
            Quad(
                bl=Vec2(l, b),
                br=Vec2(r, b),
                tl=Vec2(l, t),
                tr=Vec2(r, t),
            )
        )

    def draw_number(self, z, z2, z3):
        s_inv = 1 - self.layout1.scale
        s2_inv = 1 - self.layout2.scale

        for i in range(self.core.digit_count):
            digit = floor(self.core.combo_number / 10 ** (self.core.digit_count - 1 - i)) % 10

            digit_center_x = (
                self.layout1.start_x + (i * (self.layout1.width + self.layout1.gap)) + self.layout1.width / 2
            )
            digit_center_x2 = (
                self.layout2.start_x + (i * (self.layout2.width + self.layout2.gap)) + self.layout2.width / 2
            )

            digit_layout = self.layout_combo_number(
                l=self.layout1.scale * (digit_center_x - self.layout1.width / 2) + s_inv * self.common.center_x,
                r=self.layout1.scale * (digit_center_x + self.layout1.width / 2) + s_inv * self.common.center_x,
                t=self.layout1.scale * (self.common.center_y - self.layout1.height / 2) + s_inv * self.common.center_y,
                b=self.layout1.scale * (self.common.center_y + self.layout1.height / 2) + s_inv * self.common.center_y,
            )
            digit_layout2 = self.layout_combo_number(
                l=self.layout2.scale * (digit_center_x2 - self.layout2.width / 2) + s2_inv * self.common.center_x,
                r=self.layout2.scale * (digit_center_x2 + self.layout2.width / 2) + s2_inv * self.common.center_x,
                t=self.layout2.scale * (self.common.center_y - self.layout2.height / 2) + s2_inv * self.common.center_y,
                b=self.layout2.scale * (self.common.center_y + self.layout2.height / 2) + s2_inv * self.common.center_y,
            )

            if not self.core.ap or not Options.ap_effect:
                ActiveSkin.combo_number.get_sprite(combo=digit, combo_type=ComboType.GLOW).draw(
                    quad=digit_layout, z=z3, a=self.alpha.a3
                )
                ActiveSkin.combo_number.get_sprite(combo=digit, combo_type=ComboType.AP).draw(
                    quad=digit_layout2, z=z2, a=self.alpha.a2
                )
                ActiveSkin.combo_number.get_sprite(combo=digit, combo_type=ComboType.AP).draw(
                    quad=digit_layout, z=z, a=self.alpha.a
                )
            else:
                ActiveSkin.combo_number.get_sprite(combo=digit, combo_type=ComboType.NORMAL).draw(
                    quad=digit_layout2, z=z2, a=self.alpha.a2
                )
                ActiveSkin.combo_number.get_sprite(combo=digit, combo_type=ComboType.NORMAL).draw(
                    quad=digit_layout, z=z, a=self.alpha.a
                )


def draw_judgment_text(
    draw_time: float, judgment: Judgment, windows_bad: Interval, accuracy: float, check_pass: bool, z: float
):
    ui = runtime_ui()

    screen_center = Vec2(x=0, y=0.792)

    base_h = 0.09 * ui.combo_config.scale
    base_w = base_h * 27.3
    h, w = transform_fixed_size(base_h, base_w)
    a = ui.judgment_config.alpha * unlerp_clamped(draw_time, draw_time + 0.064, time())
    s = unlerp_clamped(draw_time, draw_time + 0.064, time())
    layout = layout_combo_label(screen_center, w=w * s / 2, h=h * s / 2)
    ActiveSkin.judgment.get_sprite(
        judgment_type=judgment, windows_bad=windows_bad, accuracy=accuracy, check_pass=check_pass
    ).draw(quad=layout, z=z, a=a)


def draw_judgment_accuracy(judgment: Judgment, accuracy: float, windows: JudgmentWindow, wrong_way: bool, z: float):
    ui = runtime_ui()

    screen_center = Vec2(x=0, y=0.723)

    base_h = 0.054 * 1.3 * ui.judgment_config.scale
    base_w = base_h * 23.6
    h, w = transform_fixed_size(base_h, base_w)
    a = ui.judgment_config.alpha
    layout = layout_combo_label(screen_center, w=w / 2, h=h / 2)
    ActiveSkin.accuracy_warning.get_sprite(
        judgment=judgment,
        windows=windows.perfect,
        accuracy=accuracy,
        wrong_way=wrong_way,
    ).draw(quad=layout, z=z, a=a)


def draw_damage_flash(draw_time: float, z: float):
    t = unlerp_clamped(draw_time, draw_time + 0.35, time())
    a = 0.768 * t**0.1 * (1 - t) ** 1.35

    for i in range(2):
        for j in range(2):
            l_val = screen().l if j == 0 else screen().r
            if i == 0:
                t_val = screen().t
            else:
                t_val = screen().b
            layout = Quad(
                bl=Vec2(l_val, 0),
                br=Vec2(0, 0),
                tl=Vec2(l_val, t_val),
                tr=Vec2(0, t_val),
            )
            ActiveSkin.damage_flash.draw(quad=layout, z=z, a=a * 0.8)
