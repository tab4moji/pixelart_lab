"""tapered_cast.py - 先細りラグビーボールのピクセル単位レイキャスト描画.

目的: 大球+小球+接円錐台の凸包を、厳密なシルエットと陰影つきで描く。
機能: 画面の各ピクセルから平行光線を飛ばし、大球・小球・円錐面との交点のうち、
      軸方向成分 s がその面の表面範囲に入るものだけを候補にして最も手前を採用する。
      陰影・縫い目・パレットは rugby(ellipsoid_model)と共通。
      範囲: 大球は s <= S_BIG、小球は s >= S_SMALL、円錐面は S_BIG <= s <= S_SMALL。

更新履歴:
  1. 2026-11-09 初版
"""

import math

import pyxel

from config import CENTER_X, CENTER_Y, SCALE
from cylinder_model import make_view, to_world
from ellipsoid_model import (SEAM_COLOR, brightness, dither_color, on_seam)
from mathutil import validate_elevation
from tapered_model import (BOUND, C_BIG, C_SMALL, R_BIG, R_SMALL, S_APEX,
                           S_BIG, S_SMALL, SLOPE_SQ, check_geometry,
                           cone_normal, sphere_normal)

EPS = 1e-9
EXTENT = int(BOUND * SCALE) + 2
KIND_BIG = "big"
KIND_SMALL = "small"
KIND_CONE = "cone"


def sphere_roots(center, radius, q_dot_a, q_sq, a_z):
    """軸上の中心 center の球との交点の t を列挙する."""
    b_half = -center * a_z
    c_coef = q_sq - 2.0 * center * q_dot_a + center * center - radius * radius
    disc = b_half * b_half - c_coef
    roots = []
    if disc >= 0.0:
        root = math.sqrt(disc)
        roots = [-b_half + root, -b_half - root]
    return roots


def cone_roots(q_dot_a, q_sq, a_z):
    """円錐面の2次方程式の解(t)を列挙する."""
    c_zero = S_APEX - q_dot_a
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


def front_hit(roots, kind, q_dot_a, a_z, low, high):
    """s が [low, high] に入る解のうち最大の t を (t, kind) で返す。無ければ None."""
    result = None
    for t_val in roots:
        s_axis = q_dot_a + t_val * a_z
        if low - EPS <= s_axis <= high + EPS:
            if result is None or t_val > result[0]:
                result = (t_val, kind)
    return result


def nearest_hit(q_dot_a, q_sq, axis):
    """全表面の最も手前の交点 (t, kind) を返す。無ければ None."""
    a_z = axis[2]
    hits = [
        front_hit(sphere_roots(C_BIG, R_BIG, q_dot_a, q_sq, a_z),
                  KIND_BIG, q_dot_a, a_z, -math.inf, S_BIG),
        front_hit(sphere_roots(C_SMALL, R_SMALL, q_dot_a, q_sq, a_z),
                  KIND_SMALL, q_dot_a, a_z, S_SMALL, math.inf),
        front_hit(cone_roots(q_dot_a, q_sq, a_z),
                  KIND_CONE, q_dot_a, a_z, S_BIG, S_SMALL),
    ]
    found = [h for h in hits if h is not None]
    result = max(found, key=lambda h: h[0]) if found else None
    return result


def hit_normal(hit, x_pos, up, q_dot_a, axis):
    """交点 hit の外向き単位法線(ビュー空間)を返す."""
    t_val, kind = hit
    s_axis = q_dot_a + t_val * axis[2]
    if kind == KIND_BIG:
        result = sphere_normal(x_pos, up, t_val, C_BIG, R_BIG, axis)
    elif kind == KIND_SMALL:
        result = sphere_normal(x_pos, up, t_val, C_SMALL, R_SMALL, axis)
    else:
        result = cone_normal(x_pos, up, t_val, s_axis, axis)
    return result


def shade_pixel(px, py, x_pos, up, view):
    """画素 (px, py) の色を返す。物体の外なら None."""
    axis = view.axis
    q_dot_a = x_pos * axis[0] + up * axis[1]
    hit = nearest_hit(q_dot_a, x_pos * x_pos + up * up, axis)
    result = None
    if hit is not None:
        _, world_y, world_z = to_world(x_pos, up, hit[0], view)
        if on_seam(world_y, world_z):
            result = SEAM_COLOR
        else:
            normal = hit_normal(hit, x_pos, up, q_dot_a, axis)
            result = dither_color(brightness(normal), px, py)
    return result


def tapered_pixels(yaw_deg, elev_deg):
    """描画対象の (px, py, 色) を列挙する."""
    check_geometry()
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


def draw_tapered(yaw_deg, elev_deg):
    """先細りラグビーボールを画面へ描く."""
    for px, py, color in tapered_pixels(yaw_deg, elev_deg):
        pyxel.pset(px, py, color)
