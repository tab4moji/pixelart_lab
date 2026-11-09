"""ellipsoid_cast.py - ラグビーボールのピクセル単位レイキャスト描画.

目的: 回転楕円体(長球)を厳密なシルエットと陰影つきで描く。
機能: 画面の各ピクセルから平行光線を飛ばし、楕円体との手前側の交点を2次方程式で求める。
      交点の法線で陰影(ディザ)を決め、子午線上は縫い目色にする。ポリゴンは使わない。
      軸方向 a と光線 (x, 上, t) の扱いは cylinder_cast.py と同じ。
      sample_pixel() は (深度 t, 色, 面ID) を返し、Z合成(composite.py)でも使う。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 shade_pixel を sample_pixel に変更し、深度 t も返すようにした
"""

import math

import pyxel

from config import CENTER_X, CENTER_Y, SCALE
from cylinder_model import make_view, to_world
from ellipsoid_model import (INV_B2, K_COEF, SEAM_COLOR, SEMI_LENGTH,
                             brightness, dither_color, on_seam,
                             surface_normal)
from mathutil import validate_elevation

EXTENT = int(SEMI_LENGTH * SCALE) + 2


def ellipsoid_depth(q_dot_a, q_sq, axis):
    """楕円体との手前側の交点の深度 t を返す。無ければ None."""
    a_z = axis[2]
    a_coef = K_COEF * a_z * a_z + INV_B2
    b_half = K_COEF * a_z * q_dot_a
    c_coef = K_COEF * q_dot_a * q_dot_a + q_sq * INV_B2 - 1.0
    disc = b_half * b_half - a_coef * c_coef
    result = None
    if disc >= 0.0:
        result = (-b_half + math.sqrt(disc)) / a_coef
    return result


def sample_pixel(px, py, x_pos, up, view):
    """画素 (px, py) の (深度 t, 色, 面ID) を返す。楕円体の外なら None."""
    axis = view.axis
    q_dot_a = x_pos * axis[0] + up * axis[1]
    t_hit = ellipsoid_depth(q_dot_a, x_pos * x_pos + up * up, axis)
    result = None
    if t_hit is not None:
        _, world_y, world_z = to_world(x_pos, up, t_hit, view)
        if on_seam(world_y, world_z):
            result = (t_hit, SEAM_COLOR, 0)
        else:
            s_axis = q_dot_a + t_hit * axis[2]
            normal = surface_normal(x_pos, up, t_hit, s_axis, axis)
            result = (t_hit, dither_color(brightness(normal), px, py), 0)
    return result


def ellipsoid_pixels(yaw_deg, elev_deg):
    """描画対象の (px, py, 色) を列挙する."""
    validate_elevation(elev_deg)
    view = make_view(yaw_deg, elev_deg)
    pixels = []
    for py in range(CENTER_Y - EXTENT, CENTER_Y + EXTENT + 1):
        up = (CENTER_Y - py) / SCALE
        for px in range(CENTER_X - EXTENT, CENTER_X + EXTENT + 1):
            hit = sample_pixel(px, py, (px - CENTER_X) / SCALE, up, view)
            if hit is not None:
                pixels.append((px, py, hit[1]))
    return pixels


def draw_ellipsoid(yaw_deg, elev_deg):
    """ラグビーボールを画面へ描く."""
    for px, py, color in ellipsoid_pixels(yaw_deg, elev_deg):
        pyxel.pset(px, py, color)
