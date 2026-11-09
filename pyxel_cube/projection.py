"""projection.py - 回転と平行投影.

目的: 立方体をY軸回転し、見下ろし角つきの平行投影で画面へ写す。
機能: project_point(): 頂点→画面座標。face_depth(): 法線の奥行き成分。
      見下ろし角 0度=真横、90度=真上から。

更新履歴:
  1. 2026-11-09 初版
"""

import math

from config import CENTER_X, CENTER_Y, SCALE
from mathutil import validate_elevation


def rotate_yaw(point, yaw_rad):
    """Y軸まわりに回転する."""
    x, y, z = point
    cos_a = math.cos(yaw_rad)
    sin_a = math.sin(yaw_rad)
    result = (x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a)
    return result


def tilt(point, elev_rad):
    """カメラ見下ろし角を適用し (x, 上方向, 手前方向) を返す."""
    x, y, z = point
    up = y * math.cos(elev_rad) - z * math.sin(elev_rad)
    depth = y * math.sin(elev_rad) + z * math.cos(elev_rad)
    result = (x, up, depth)
    return result


def project_point(point, yaw_deg, elev_deg):
    """3D頂点を画面のピクセル座標 (sx, sy) へ投影する."""
    validate_elevation(elev_deg)
    rotated = rotate_yaw(point, math.radians(yaw_deg))
    x, up, _ = tilt(rotated, math.radians(elev_deg))
    result = (round(CENTER_X + x * SCALE), round(CENTER_Y - up * SCALE))
    return result


def face_depth(normal, yaw_deg, elev_deg):
    """法線の手前方向成分を返す。正ならカメラ側を向く."""
    validate_elevation(elev_deg)
    rotated = rotate_yaw(normal, math.radians(yaw_deg))
    _, _, depth = tilt(rotated, math.radians(elev_deg))
    return depth
