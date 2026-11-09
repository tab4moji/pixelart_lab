"""tapered_model.py - 先細りラグビーボール(大球+小球+接円錐台の凸包)の寸法と法線.

目的: 軸がX方向の横向き先細りラグビーボールを、解析式で扱うための定数と法線計算を提供する。
機能: 大球(-X側)と小球(+X側)、およびその2球に外接する円錐台の凸包を表す。
      接円錐の半頂角を a とすると sin(a) = (R_BIG - R_SMALL) / CENTER_DIST。
      球面は軸方向成分 s が接点より外側の部分、円錐面は s が S_BIG〜S_SMALL の部分だけが表面になる。
      全体の軸方向の幅が原点中心になるよう、2球の中心位置を決める。
      円錐面の式: |P|^2 - s^2 = m^2 (S_APEX - s)^2  (m = tan(a))。

更新履歴:
  1. 2026-11-09 初版
"""

import math

R_BIG = 0.85
R_SMALL = 0.4
CENTER_DIST = 1.5

HALF_SPAN = (R_BIG + CENTER_DIST + R_SMALL) / 2.0
C_BIG = -HALF_SPAN + R_BIG
C_SMALL = C_BIG + CENTER_DIST

SIN_A = (R_BIG - R_SMALL) / CENTER_DIST
COS_A = math.sqrt(max(0.0, 1.0 - SIN_A * SIN_A))
SLOPE = SIN_A / COS_A if COS_A > 0.0 else 0.0
SLOPE_SQ = SLOPE * SLOPE

S_BIG = C_BIG + R_BIG * SIN_A
S_SMALL = C_SMALL + R_SMALL * SIN_A
S_APEX = S_BIG + R_BIG * COS_A / SLOPE if SLOPE > 0.0 else 0.0

BOUND = max(abs(C_BIG) + R_BIG, abs(C_SMALL) + R_SMALL)
MIN_NORM = 1e-9


def check_geometry():
    """2球が一方を包含しない配置か検証する。不正なら ValueError."""
    if CENTER_DIST <= abs(R_BIG - R_SMALL):
        raise ValueError("one sphere contains the other")
    result = True
    return result


def sphere_normal(x_pos, up, depth, center, radius, axis):
    """球面上の点の外向き単位法線(ビュー空間)を返す."""
    result = ((x_pos - center * axis[0]) / radius,
              (up - center * axis[1]) / radius,
              (depth - center * axis[2]) / radius)
    return result


def cone_normal(x_pos, up, depth, s_axis, axis):
    """円錐面上の点の外向き単位法線(ビュー空間)を返す."""
    k_val = s_axis - SLOPE_SQ * (S_APEX - s_axis)
    n_x = x_pos - k_val * axis[0]
    n_y = up - k_val * axis[1]
    n_z = depth - k_val * axis[2]
    norm = max(math.sqrt(n_x * n_x + n_y * n_y + n_z * n_z), MIN_NORM)
    result = (n_x / norm, n_y / norm, n_z / norm)
    return result
