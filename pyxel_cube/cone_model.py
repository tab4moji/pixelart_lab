"""cone_model.py - 円錐の寸法・配色・陰影.

目的: 軸がX方向の横向き円錐を、解析式で扱うための定数と陰影計算を提供する。
機能: 頂点は +X 側、底面は -X 側。side_normal() が側面の法線(ビュー空間)を返し、
      dither_ramp() が明るさを指定パレットのベイヤー配列ディザ色に変換する。
      明るさの計算(brightness)とディザ行列(BAYER)は ellipsoid_model を共用する。
      側面の式: |P|^2 - s^2 = m^2 (H - s)^2  (s は軸方向成分、m = R / (2H))。

更新履歴:
  1. 2026-11-09 初版
"""

import math

from ellipsoid_model import BAYER

HALF_HEIGHT = 1.2
BASE_RADIUS = 0.9
SLOPE_SQ = (BASE_RADIUS / (2.0 * HALF_HEIGHT)) ** 2

SIDE_RAMP = (1, 5, 12, 6)
CAP_RAMP = (1, 3, 11, 7)
MIN_NORM = 1e-9


def side_normal(x_pos, up, depth, s_axis, axis):
    """側面上の点 (x, 上, 手前) の外向き単位法線(ビュー空間)を返す."""
    k_val = s_axis - SLOPE_SQ * (HALF_HEIGHT - s_axis)
    n_x = x_pos - k_val * axis[0]
    n_y = up - k_val * axis[1]
    n_z = depth - k_val * axis[2]
    norm = max(math.sqrt(n_x * n_x + n_y * n_y + n_z * n_z), MIN_NORM)
    result = (n_x / norm, n_y / norm, n_z / norm)
    return result


def dither_ramp(ramp, value, px, py):
    """明るさ(0〜1)をベイヤー配列ディザで ramp の色に変換する."""
    pos = max(0.0, min(1.0, value)) * (len(ramp) - 1)
    base = min(int(pos), len(ramp) - 2)
    threshold = (BAYER[py % 4][px % 4] + 0.5) / 16.0
    result = ramp[base + 1] if pos - base > threshold else ramp[base]
    return result
