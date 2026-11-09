"""poly_cast.py - 凸多面体の光線との交点計算(Z合成用).

目的: 立方体系(cube / wedge / slant)を、ポリゴンではなく光線との交点で
      (深度 t, 色, 面ID) として返し、他形状と同じ Z バッファで合成できるようにする。
機能: 面は (頂点index列, 外向き法線, 色)。平面は n・P <= d (d = n・最初の頂点)。
      光線 P = q + t e (ワールド座標、q は画素位置 (x, 上) の線形関数) について、
      法線が光線側を向く面(n・e > 0)の最小の t が表面(カメラ側の出口)、
      その反対側の面の最大の t が入口。入口 <= 出口なら交差し、表面の面の色とIDを返す。
      法線は符号と比のみ使うので正規化は不要。
      prepare_planes() でフレームごとに n・q の係数と n・e を前計算し、画素ごとの計算を軽くする。

更新履歴:
  1. 2026-11-09 初版
"""

import math

from cylinder_model import to_world

EPS = 1e-9


def build_planes(vertices, faces):
    """面データから (法線, 平面定数 d, 面ID, 色) のリストを作る."""
    planes = []
    for face_id, (indices, normal, color) in enumerate(faces):
        point = vertices[indices[0]]
        offset = sum(n * p for n, p in zip(normal, point))
        planes.append((normal, offset, face_id, color))
    return planes


def dot(vec_a, vec_b):
    """3次元ベクトルの内積."""
    result = vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1] + vec_a[2] * vec_b[2]
    return result


def prepare_planes(planes, view):
    """view 用に (c_x, c_y, d, n・e, 面ID, 色) を前計算する.

    画素位置 (x, 上) のワールド座標は x * W_x + 上 * W_y なので、
    n・q = x * (n・W_x) + 上 * (n・W_y) になる。
    """
    axis_x = to_world(1.0, 0.0, 0.0, view)
    axis_y = to_world(0.0, 1.0, 0.0, view)
    direction = to_world(0.0, 0.0, 1.0, view)
    prepared = []
    for normal, offset, face_id, color in planes:
        prepared.append((dot(normal, axis_x), dot(normal, axis_y), offset,
                         dot(normal, direction), face_id, color))
    return prepared


def ray_convex(prepared, x_pos, up):
    """凸多面体と光線の表面交点 (t, 色, 面ID) を返す。交差しなければ None."""
    t_exit = math.inf
    t_enter = -math.inf
    front = None
    inside = True
    for c_x, c_y, offset, rate, face_id, color in prepared:
        slack = offset - (x_pos * c_x + up * c_y)
        if abs(rate) < EPS:
            inside = inside and slack >= 0.0
        elif rate > 0.0:
            t_val = slack / rate
            if t_val < t_exit:
                t_exit = t_val
                front = (face_id, color)
        else:
            t_enter = max(t_enter, slack / rate)
    result = None
    if inside and front is not None and t_enter <= t_exit:
        result = (t_exit, front[1], front[0])
    return result


def make_poly_sampler(planes, view):
    """この view 用の sampler(px, py, x_pos, up) を返す."""
    prepared = prepare_planes(planes, view)

    def sample(px, py, x_pos, up):
        return ray_convex(prepared, x_pos, up)

    return sample
