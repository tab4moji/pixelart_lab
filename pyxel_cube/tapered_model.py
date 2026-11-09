"""tapered_model.py - 先細りラグビーボール(大球+小球+接円錐台の凸包)の寸法と法線.

目的: 軸がX方向の横向き先細りラグビーボールを、解析式で扱うための形状パラメータと法線計算を提供する。
機能: 大球(-X側、半径固定)と小球(+X側、半径可変)、およびその2球に外接する円錐台の凸包を表す。
      make_geometry(ratio) が小球半径 = 大球半径 x ratio の形状(Geometry)を返す。
      ratio = 0 で小球は点(大球に接する円錐)、ratio = 1 で両端が同じ半径(円柱+半球2つ)。
      ratio_from_level() は 1〜5 の段階を ratio(0, 0.25, 0.5, 0.75, 1)へ変換する。
      接円錐の半頂角を a とすると sin(a) = (R_BIG - r_small) / CENTER_DIST。
      円錐面の半径は r(s) = intercept - slope * s (s は軸方向成分)。slope = tan(a)。
      slope = 0 のときは円柱になるため、頂点(S_APEX)は使わず intercept で表す。
      全体の軸方向の幅が原点中心になるよう、2球の中心位置を決める。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 小球半径を可変にし、円錐面を intercept 形式へ一般化
"""

import math
from collections import namedtuple

R_BIG = 0.85
R_SMALL_DEFAULT = 0.4
DEFAULT_RATIO = R_SMALL_DEFAULT / R_BIG
CENTER_DIST = 1.5
LEVEL_MIN = 1
LEVEL_MAX = 5
MIN_NORM = 1e-9

Geometry = namedtuple(
    "Geometry",
    "r_small c_big c_small slope intercept s_big s_small bound")


def ratio_from_level(level):
    """段階 1〜5 を小球/大球の半径比 0〜1 へ変換する。範囲外は ValueError."""
    if not LEVEL_MIN <= level <= LEVEL_MAX:
        raise ValueError(f"level out of range: {level}")
    result = (level - LEVEL_MIN) / (LEVEL_MAX - LEVEL_MIN)
    return result


def make_geometry(ratio):
    """小球半径 = R_BIG * ratio の形状を返す。不正な ratio は ValueError."""
    if not 0.0 <= ratio <= 1.0:
        raise ValueError(f"ratio out of range: {ratio}")
    r_small = R_BIG * ratio
    half_span = (R_BIG + CENTER_DIST + r_small) / 2.0
    c_big = -half_span + R_BIG
    c_small = c_big + CENTER_DIST
    sin_a = (R_BIG - r_small) / CENTER_DIST
    cos_a = math.sqrt(1.0 - sin_a * sin_a)
    slope = sin_a / cos_a
    s_big = c_big + R_BIG * sin_a
    s_small = c_small + r_small * sin_a
    intercept = R_BIG * cos_a + slope * s_big
    bound = max(abs(c_big) + R_BIG, abs(c_small) + r_small)
    result = Geometry(r_small, c_big, c_small, slope, intercept,
                      s_big, s_small, bound)
    return result


def sphere_normal(x_pos, up, depth, center, radius, axis):
    """球面上の点の外向き単位法線(ビュー空間)を返す."""
    result = ((x_pos - center * axis[0]) / radius,
              (up - center * axis[1]) / radius,
              (depth - center * axis[2]) / radius)
    return result


def cone_normal(x_pos, up, depth, s_axis, axis, geo):
    """円錐(円柱)面上の点の外向き単位法線(ビュー空間)を返す."""
    radius = geo.intercept - geo.slope * s_axis
    k_val = s_axis - geo.slope * radius
    n_x = x_pos - k_val * axis[0]
    n_y = up - k_val * axis[1]
    n_z = depth - k_val * axis[2]
    norm = max(math.sqrt(n_x * n_x + n_y * n_y + n_z * n_z), MIN_NORM)
    result = (n_x / norm, n_y / norm, n_z / norm)
    return result
