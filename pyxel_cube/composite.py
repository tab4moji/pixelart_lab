"""composite.py - 複数形状の Z バッファ合成.

目的: 選択された複数の形状を、画素ごとの深度(Zバッファ)で合成して描く。
機能: 各形状の sampler を全画素に当て、深度 t が最大(最も手前)の結果を残す。
      立方体系(輪郭フラグ True)は、異なる面や別の形状・背景との境界の画素を
      輪郭色にする。境界を挟む2画素のうち片側だけを輪郭にして線幅を1画素に保つ
      (相手も輪郭対象なら面IDの大きい側、相手が対象外や背景ならこちら側)。
      composite_pixels() は描画せずに (px, py, 色) を返し、draw_composite() が描く。

更新履歴:
  1. 2026-11-09 初版
"""

import pyxel

from config import CENTER_X, CENTER_Y, EDGE_COLOR, SCALE
from cylinder_model import make_view
from mathutil import validate_elevation
from samplers import build_entries

NEIGHBORS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def keep_nearest(best, key, record):
    """record = (深度, 色, 識別子, 輪郭フラグ) が手前なら best[key] を更新する."""
    current = best.get(key)
    if current is None or record[0] > current[0]:
        best[key] = record


def scan_entry(best, index, entry):
    """1形状を全画素に当て、Zバッファ best を更新する."""
    sampler, extent, outline = entry
    for py in range(CENTER_Y - extent, CENTER_Y + extent + 1):
        up = (CENTER_Y - py) / SCALE
        for px in range(CENTER_X - extent, CENTER_X + extent + 1):
            hit = sampler(px, py, (px - CENTER_X) / SCALE, up)
            if hit is not None:
                keep_nearest(best, (px, py),
                             (hit[0], hit[1], (index, hit[2]), outline))


def border_with(ident, other):
    """識別子 ident の画素が、隣 other との境界で輪郭になるか."""
    if other is None:
        result = True
    elif other[2] == ident:
        result = False
    elif not other[3]:
        result = True
    else:
        result = ident > other[2]
    return result


def is_edge(best, px, py, record):
    """画素 (px, py) が輪郭線になるか(輪郭対象の形状のみ)."""
    result = False
    if record[3]:
        for d_x, d_y in NEIGHBORS:
            other = best.get((px + d_x, py + d_y))
            if border_with(record[2], other):
                result = True
    return result


def composite_pixels(yaw_deg, elev_deg, names, ratio):
    """names の形状を Z 合成した (px, py, 色) を返す."""
    validate_elevation(elev_deg)
    view = make_view(yaw_deg, elev_deg)
    best = {}
    for index, entry in enumerate(build_entries(names, view, ratio)):
        scan_entry(best, index, entry)
    pixels = []
    for (px, py), record in best.items():
        color = EDGE_COLOR if is_edge(best, px, py, record) else record[1]
        pixels.append((px, py, color))
    return pixels


def draw_composite(yaw_deg, elev_deg, names, ratio):
    """names の形状を Z 合成して画面へ描く."""
    for px, py, color in composite_pixels(yaw_deg, elev_deg, names, ratio):
        pyxel.pset(px, py, color)
