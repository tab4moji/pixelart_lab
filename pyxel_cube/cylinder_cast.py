"""cylinder_cast.py - 円柱のピクセル単位レイキャスト描画.

目的: 円柱を厳密なシルエット(端の楕円と側面)で描く。
機能: 画面の各ピクセルから平行光線を飛ばし、円柱の側面・両端キャップとの交点のうち
      最も手前を採用して色を決める。ポリゴンを使わないので外側へのはみ出しが出ない。
      軸方向はビュー空間で a、光線は (x, 上, t)(tが大きいほど手前)。

更新履歴:
  1. 2026-11-09 初版
"""

import math

import pyxel

from config import CENTER_X, CENTER_Y, SCALE
from cylinder_model import (CAP_COLOR, HALF_LENGTH, RADIUS, make_view,
                            stripe_color, to_world)
from mathutil import validate_elevation

EPS = 1e-9
EXTENT = int(math.hypot(HALF_LENGTH, RADIUS) * SCALE) + 2


def side_depth(q_dot_a, q_sq, axis):
    """側面との手前側の交点の深度 t を返す。無ければ None."""
    a_z = axis[2]
    a_coef = 1.0 - a_z * a_z
    result = None
    if a_coef > EPS:
        b_half = -a_z * q_dot_a
        c_coef = q_sq - q_dot_a * q_dot_a - RADIUS * RADIUS
        disc = b_half * b_half - a_coef * c_coef
        if disc >= 0.0:
            t_near = (-b_half + math.sqrt(disc)) / a_coef
            if abs(q_dot_a + t_near * a_z) <= HALF_LENGTH:
                result = t_near
    return result


def cap_depth(q_dot_a, q_sq, axis):
    """両端キャップとの交点のうち最も手前の深度 t を返す。無ければ None."""
    a_z = axis[2]
    result = None
    if abs(a_z) > EPS:
        for sign in (1.0, -1.0):
            t_cap = (sign * HALF_LENGTH - q_dot_a) / a_z
            radial_sq = q_sq + t_cap * t_cap - HALF_LENGTH * HALF_LENGTH
            if radial_sq <= RADIUS * RADIUS:
                if result is None or t_cap > result:
                    result = t_cap
    return result


def shade_pixel(x_pos, up, view):
    """ビュー空間の位置 (x, 上) の画素色を返す。円柱外なら None."""
    axis = view.axis
    q_dot_a = x_pos * axis[0] + up * axis[1]
    q_sq = x_pos * x_pos + up * up
    t_side = side_depth(q_dot_a, q_sq, axis)
    t_cap = cap_depth(q_dot_a, q_sq, axis)
    result = None
    if t_side is not None and (t_cap is None or t_side >= t_cap):
        _, world_y, world_z = to_world(x_pos, up, t_side, view)
        result = stripe_color(world_y, world_z)
    elif t_cap is not None:
        result = CAP_COLOR
    return result


def cylinder_pixels(yaw_deg, elev_deg):
    """描画対象の (px, py, 色) を列挙する."""
    validate_elevation(elev_deg)
    view = make_view(yaw_deg, elev_deg)
    pixels = []
    for py in range(CENTER_Y - EXTENT, CENTER_Y + EXTENT + 1):
        up = (CENTER_Y - py) / SCALE
        for px in range(CENTER_X - EXTENT, CENTER_X + EXTENT + 1):
            color = shade_pixel((px - CENTER_X) / SCALE, up, view)
            if color is not None:
                pixels.append((px, py, color))
    return pixels


def draw_cylinder(yaw_deg, elev_deg):
    """円柱を画面へ描く."""
    for px, py, color in cylinder_pixels(yaw_deg, elev_deg):
        pyxel.pset(px, py, color)
