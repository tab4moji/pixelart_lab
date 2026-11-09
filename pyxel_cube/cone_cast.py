"""cone_cast.py - 円錐のピクセル単位レイキャスト描画.

目的: 横向き円錐を厳密なシルエットと陰影つきで描く。
機能: 画面の各ピクセルから平行光線を飛ばし、側面(2次方程式)と底面(平面)との交点のうち
      最も手前を採用する。側面は法線で陰影、底面は -軸方向の法線で陰影を付ける。
      側面の2次方程式は両側の円錐(頂点の向こう側)も解に含むため、軸方向成分 s が
      [-H, H] に入る解だけを採る。

更新履歴:
  1. 2026-11-09 初版
"""

import math

import pyxel

from config import CENTER_X, CENTER_Y, SCALE
from cone_model import (BASE_RADIUS, CAP_RAMP, HALF_HEIGHT, SIDE_RAMP,
                        SLOPE_SQ, dither_ramp, side_normal)
from cylinder_model import make_view
from ellipsoid_model import brightness
from mathutil import validate_elevation

EPS = 1e-9
EXTENT = int(math.hypot(HALF_HEIGHT, BASE_RADIUS) * SCALE) + 2


def side_roots(q_dot_a, q_sq, axis):
    """側面の2次方程式の解(t)を列挙する."""
    a_z = axis[2]
    c_zero = HALF_HEIGHT - q_dot_a
    a_coef = 1.0 - a_z * a_z * (1.0 + SLOPE_SQ)
    b_half = a_z * (SLOPE_SQ * c_zero - q_dot_a)
    c_coef = q_sq - q_dot_a * q_dot_a - SLOPE_SQ * c_zero * c_zero
    roots = []
    if abs(a_coef) > EPS:
        disc = b_half * b_half - a_coef * c_coef
        if disc >= 0.0:
            root = math.sqrt(disc)
            roots = [(-b_half + root) / a_coef, (-b_half - root) / a_coef]
    elif abs(b_half) > EPS:
        roots = [-c_coef / (2.0 * b_half)]
    return roots


def side_depth(q_dot_a, q_sq, axis):
    """側面との最も手前の交点の深度 t を返す。無ければ None."""
    result = None
    for t_val in side_roots(q_dot_a, q_sq, axis):
        s_axis = q_dot_a + t_val * axis[2]
        if abs(s_axis) <= HALF_HEIGHT:
            if result is None or t_val > result:
                result = t_val
    return result


def cap_depth(q_dot_a, q_sq, axis):
    """底面(s = -H)との交点の深度 t を返す。無ければ None."""
    a_z = axis[2]
    result = None
    if abs(a_z) > EPS:
        t_cap = (-HALF_HEIGHT - q_dot_a) / a_z
        radial_sq = q_sq + t_cap * t_cap - HALF_HEIGHT * HALF_HEIGHT
        if radial_sq <= BASE_RADIUS * BASE_RADIUS:
            result = t_cap
    return result


def shade_pixel(px, py, x_pos, up, view):
    """画素 (px, py) の色を返す。円錐の外なら None."""
    axis = view.axis
    q_dot_a = x_pos * axis[0] + up * axis[1]
    q_sq = x_pos * x_pos + up * up
    t_side = side_depth(q_dot_a, q_sq, axis)
    t_cap = cap_depth(q_dot_a, q_sq, axis)
    result = None
    if t_side is not None and (t_cap is None or t_side >= t_cap):
        s_axis = q_dot_a + t_side * axis[2]
        normal = side_normal(x_pos, up, t_side, s_axis, axis)
        result = dither_ramp(SIDE_RAMP, brightness(normal), px, py)
    elif t_cap is not None:
        normal = (-axis[0], -axis[1], -axis[2])
        result = dither_ramp(CAP_RAMP, brightness(normal), px, py)
    return result


def cone_pixels(yaw_deg, elev_deg):
    """描画対象の (px, py, 色) を列挙する."""
    validate_elevation(elev_deg)
    view = make_view(yaw_deg, elev_deg)
    pixels = []
    for py in range(CENTER_Y - EXTENT, CENTER_Y + EXTENT + 1):
        up = (CENTER_Y - py) / SCALE
        for px in range(CENTER_X - EXTENT, CENTER_X + EXTENT + 1):
            color = shade_pixel(px, py, (px - CENTER_X) / SCALE, up, view)
            if color is not None:
                pixels.append((px, py, color))
    return pixels


def draw_cone(yaw_deg, elev_deg):
    """円錐を画面へ描く."""
    for px, py, color in cone_pixels(yaw_deg, elev_deg):
        pyxel.pset(px, py, color)
