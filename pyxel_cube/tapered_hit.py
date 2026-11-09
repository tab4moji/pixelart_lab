"""tapered_hit.py - 先細りラグビーボールの光線との交点計算.

目的: 平行光線と、大球・小球・円錐(円柱)面との最も手前の交点を求める。
機能: 光線は P = q + t e_z。軸方向成分 s = qa + a_z t。
      球: t^2 - 2 c a_z t + (q2 - 2 c qa + c^2 - r^2) = 0。
      円錐面: A t^2 + 2 (B/2) t + C = 0 (e0 = intercept - slope * qa として
      A = 1 - a_z^2 (1 + m^2)、B/2 = a_z (m e0 - qa)、C = q2 - qa^2 - e0^2)。
      各面は軸方向成分 s が表面範囲に入る解だけを採る。
      範囲: 大球は s <= S_BIG、小球は s >= S_SMALL、円錐面は S_BIG <= s <= S_SMALL。
      小球の半径が 0(点)のときは小球を判定から除く。

更新履歴:
  1. 2026-11-09 初版(tapered_cast.py から分離し、可変形状に対応)
"""

import math

from tapered_model import R_BIG, cone_normal, sphere_normal

EPS = 1e-9
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


def cone_roots(q_dot_a, q_sq, a_z, geo):
    """円錐(円柱)面の2次方程式の解(t)を列挙する."""
    slope = geo.slope
    e_zero = geo.intercept - slope * q_dot_a
    a_coef = 1.0 - a_z * a_z * (1.0 + slope * slope)
    b_half = a_z * (slope * e_zero - q_dot_a)
    c_coef = q_sq - q_dot_a * q_dot_a - e_zero * e_zero
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


def nearest_hit(q_dot_a, q_sq, axis, geo):
    """全表面の最も手前の交点 (t, kind) を返す。無ければ None."""
    a_z = axis[2]
    hits = [
        front_hit(sphere_roots(geo.c_big, R_BIG, q_dot_a, q_sq, a_z),
                  KIND_BIG, q_dot_a, a_z, -math.inf, geo.s_big),
        front_hit(cone_roots(q_dot_a, q_sq, a_z, geo),
                  KIND_CONE, q_dot_a, a_z, geo.s_big, geo.s_small),
    ]
    if geo.r_small > EPS:
        roots = sphere_roots(geo.c_small, geo.r_small, q_dot_a, q_sq, a_z)
        hits.append(front_hit(roots, KIND_SMALL, q_dot_a, a_z,
                              geo.s_small, math.inf))
    found = [h for h in hits if h is not None]
    result = max(found, key=lambda h: h[0]) if found else None
    return result


def hit_normal(hit, x_pos, up, q_dot_a, axis, geo):
    """交点 hit の外向き単位法線(ビュー空間)を返す."""
    t_val, kind = hit
    s_axis = q_dot_a + t_val * axis[2]
    if kind == KIND_BIG:
        result = sphere_normal(x_pos, up, t_val, geo.c_big, R_BIG, axis)
    elif kind == KIND_SMALL:
        result = sphere_normal(x_pos, up, t_val, geo.c_small, geo.r_small,
                               axis)
    else:
        result = cone_normal(x_pos, up, t_val, s_axis, axis, geo)
    return result
