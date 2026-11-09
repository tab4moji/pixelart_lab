"""tapered_cast.py - 先細りラグビーボールのピクセル単位レイキャスト描画.

目的: 大球+小球+接円錐台の凸包を、厳密なシルエットと陰影つきで描く。
機能: 画面の各ピクセルから平行光線を飛ばし、tapered_hit の最も手前の交点で色を決める。
      小球の大きさは ratio(小球半径/大球半径、0〜1)で指定する。
      陰影・縫い目・パレットは rugby(ellipsoid_model)と共通。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 ratio 引数を追加、交点計算を tapered_hit.py へ分離
"""

import pyxel

from config import CENTER_X, CENTER_Y, SCALE
from cylinder_model import make_view, to_world
from ellipsoid_model import SEAM_COLOR, brightness, dither_color, on_seam
from mathutil import validate_elevation
from tapered_hit import hit_normal, nearest_hit
from tapered_model import DEFAULT_RATIO, make_geometry


def shade_pixel(px, py, x_pos, up, view, geo):
    """画素 (px, py) の色を返す。物体の外なら None."""
    axis = view.axis
    q_dot_a = x_pos * axis[0] + up * axis[1]
    hit = nearest_hit(q_dot_a, x_pos * x_pos + up * up, axis, geo)
    result = None
    if hit is not None:
        _, world_y, world_z = to_world(x_pos, up, hit[0], view)
        if on_seam(world_y, world_z):
            result = SEAM_COLOR
        else:
            normal = hit_normal(hit, x_pos, up, q_dot_a, axis, geo)
            result = dither_color(brightness(normal), px, py)
    return result


def tapered_pixels(yaw_deg, elev_deg, ratio=DEFAULT_RATIO):
    """描画対象の (px, py, 色) を列挙する."""
    validate_elevation(elev_deg)
    geo = make_geometry(ratio)
    extent = int(geo.bound * SCALE) + 2
    view = make_view(yaw_deg, elev_deg)
    pixels = []
    for py in range(CENTER_Y - extent, CENTER_Y + extent + 1):
        up = (CENTER_Y - py) / SCALE
        for px in range(CENTER_X - extent, CENTER_X + extent + 1):
            color = shade_pixel(px, py, (px - CENTER_X) / SCALE, up, view,
                                geo)
            if color is not None:
                pixels.append((px, py, color))
    return pixels


def draw_tapered(yaw_deg, elev_deg, ratio=DEFAULT_RATIO):
    """先細りラグビーボールを画面へ描く."""
    for px, py, color in tapered_pixels(yaw_deg, elev_deg, ratio):
        pyxel.pset(px, py, color)
