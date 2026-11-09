"""cylinder_model.py - 円柱の寸法・配色・ビュー変換.

目的: 軸がX方向の横向き円柱を、解析的な式で扱うための定数とビュー情報を提供する。
機能: make_view() が回転・見下ろし角の三角関数と軸方向をまとめた View を返す。
      to_world() はビュー空間の点をワールド座標へ戻し、stripe_color() が縞の色を決める。
      ポリゴン近似は使わない(整数頂点と塗りの端処理による外側ピクセルを避けるため)。

更新履歴:
  1. 2026-11-09 初版(16角柱近似)
  2. 2026-11-09 解析的な円柱(レイキャスト用)に全面変更
"""

import math
from collections import namedtuple

from projection import rotate_yaw, tilt

RADIUS = 0.9
HALF_LENGTH = 1.2
STRIPES = 16
SIDE_COLORS = (10, 11)
CAP_COLOR = 12

View = namedtuple("View", "axis cos_a sin_a cos_e sin_e")


def make_view(yaw_deg, elev_deg):
    """軸方向(ビュー空間)と三角関数をまとめた View を返す."""
    yaw = math.radians(yaw_deg)
    elev = math.radians(elev_deg)
    axis = tilt(rotate_yaw((1.0, 0.0, 0.0), yaw), elev)
    result = View(axis, math.cos(yaw), math.sin(yaw),
                  math.cos(elev), math.sin(elev))
    return result


def to_world(x_pos, up, depth, view):
    """ビュー空間(x, 上, 手前)の点をワールド座標(X, Y, Z)へ戻す."""
    world_y = up * view.cos_e + depth * view.sin_e
    z_yawed = -up * view.sin_e + depth * view.cos_e
    world_x = x_pos * view.cos_a - z_yawed * view.sin_a
    world_z = x_pos * view.sin_a + z_yawed * view.cos_a
    return (world_x, world_y, world_z)


def stripe_color(world_y, world_z):
    """円周方向の角度から縞の色を返す."""
    angle = math.atan2(world_z, world_y) % (2.0 * math.pi)
    index = int(angle / (2.0 * math.pi / STRIPES))
    result = SIDE_COLORS[index % len(SIDE_COLORS)]
    return result
