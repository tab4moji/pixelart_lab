"""ellipsoid_model.py - ラグビーボール(長球)の寸法・配色・陰影.

目的: 軸がX方向の横向きラグビーボールを、回転楕円体の解析式で扱うための定数と陰影計算を提供する。
機能: surface_normal() が表面の法線(ビュー空間)を返し、brightness() がランバート拡散で明るさを、
      dither_color() が明るさを4段階パレット+ベイヤー配列ディザの色に変換する。
      on_seam() は子午線(4本)の縫い目判定を行う。ビュー変換は cylinder_model を共用する。
      式: s^2/a^2 + (|P|^2 - s^2)/b^2 = 1  (s は軸方向成分、a は半長、b は半径)。

更新履歴:
  1. 2026-11-09 初版
"""

import math

SEMI_LENGTH = 1.35
SEMI_RADIUS = 0.85
INV_B2 = 1.0 / (SEMI_RADIUS * SEMI_RADIUS)
K_COEF = 1.0 / (SEMI_LENGTH * SEMI_LENGTH) - INV_B2

RAMP = (1, 4, 9, 15)
SEAM_COLOR = 2
SEAM_HALF_WIDTH = 0.06
AMBIENT = 0.12
LIGHT = (-0.45, 0.6, 0.66)

BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


def surface_normal(x_pos, up, depth, s_axis, axis):
    """点 (x, 上, 手前) における外向き単位法線(ビュー空間)を返す."""
    n_x = x_pos * INV_B2 + K_COEF * s_axis * axis[0]
    n_y = up * INV_B2 + K_COEF * s_axis * axis[1]
    n_z = depth * INV_B2 + K_COEF * s_axis * axis[2]
    norm = math.sqrt(n_x * n_x + n_y * n_y + n_z * n_z)
    result = (n_x / norm, n_y / norm, n_z / norm)
    return result


def brightness(normal):
    """ランバート拡散+環境光による明るさ(0〜1)を返す."""
    lambert = max(0.0, sum(n * l for n, l in zip(normal, LIGHT)))
    result = AMBIENT + (1.0 - AMBIENT) * lambert
    return result


def dither_color(value, px, py):
    """明るさ(0〜1)をベイヤー配列ディザでパレット色に変換する."""
    pos = max(0.0, min(1.0, value)) * (len(RAMP) - 1)
    base = min(int(pos), len(RAMP) - 2)
    threshold = (BAYER[py % 4][px % 4] + 0.5) / 16.0
    result = RAMP[base + 1] if pos - base > threshold else RAMP[base]
    return result


def on_seam(world_y, world_z):
    """円周角が 90 度刻みの子午線(縫い目)に近いか判定する."""
    quarter = math.atan2(world_z, world_y) / (math.pi / 2.0)
    dist = abs(quarter - round(quarter)) * (math.pi / 2.0)
    result = dist < SEAM_HALF_WIDTH
    return result
