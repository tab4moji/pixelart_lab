"""cylinder_model.py - 円柱(N角柱近似)のモデル生成.

目的: 輸がX方向の横向き円柱を、N角柱として頂点・面データに変換する。
機能: build_cylinder() が (頂点列, 面列) を返す。側面は四角形を周方向にN枚、
      両端はN角形のキャップを2枚。側面は縞模様に2色を交互に割り当てる。
      法線は側面の中心角方向、キャップは±X。面の形式は cube_model.py と同じ。

更新履歴:
  1. 2026-11-09 初版
"""

import math

SIDE_COLORS = (10, 11)
CAP_COLOR = 12


def ring_vertices(x_pos, segments, radius):
    """X=x_pos の平面上の円周頂点列を返す."""
    step = 2.0 * math.pi / segments
    result = [(x_pos, radius * math.cos(step * i), radius * math.sin(step * i))
              for i in range(segments)]
    return result


def side_face(index, segments):
    """周方向 index 番目の側面(四角形)を返す."""
    nxt = (index + 1) % segments
    mid = 2.0 * math.pi * (index + 0.5) / segments
    indices = (index, nxt, segments + nxt, segments + index)
    normal = (0.0, math.cos(mid), math.sin(mid))
    color = SIDE_COLORS[index % len(SIDE_COLORS)]
    result = (indices, normal, color)
    return result


def build_cylinder(segments=16, radius=0.9, half_length=1.2):
    """横向き円柱の (頂点列, 面列) を生成する."""
    if segments < 4 or segments % 2:
        raise ValueError(f"segments must be even and >= 4: {segments}")
    vertices = (ring_vertices(-half_length, segments, radius)
                + ring_vertices(half_length, segments, radius))
    sides = [side_face(i, segments) for i in range(segments)]
    cap_neg = (tuple(range(segments)), (-1.0, 0.0, 0.0), CAP_COLOR)
    cap_pos = (tuple(range(segments, 2 * segments)),
               (1.0, 0.0, 0.0), CAP_COLOR)
    result = (tuple(vertices), tuple(sides) + (cap_neg, cap_pos))
    return result
