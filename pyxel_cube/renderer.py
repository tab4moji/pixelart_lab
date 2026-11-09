"""renderer.py - 立体の描画.

目的: 投影済み頂点から面と辺を Pyxel で描く。
機能: 背面カリング(法線の手前成分>0の面のみ)、多角形塗り(扇状三角形分割)、
      輪郭線。三角形と四角形の面を扱う。凸形状なので描画順は不問。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 面データを引数化し三角形面に対応
"""

import pyxel

from config import EDGE_COLOR, VISIBLE_EPS
from cube_model import VERTICES
from projection import face_depth, project_point


def fill_polygon(pts, color):
    """多角形を扇状に三角形分割して塗る."""
    x0, y0 = pts[0]
    for i in range(1, len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        pyxel.tri(x0, y0, x1, y1, x2, y2, color)


def outline_polygon(pts, color):
    """多角形の輪郭線を引く."""
    for i, (x0, y0) in enumerate(pts):
        x1, y1 = pts[(i + 1) % len(pts)]
        pyxel.line(x0, y0, x1, y1, color)


def draw_face(face, yaw_deg, elev_deg):
    """カメラ側を向く面だけ描画する."""
    indices, normal, color = face
    if face_depth(normal, yaw_deg, elev_deg) > VISIBLE_EPS:
        pts = [project_point(VERTICES[i], yaw_deg, elev_deg)
               for i in indices]
        fill_polygon(pts, color)
        outline_polygon(pts, EDGE_COLOR)


def draw_shape(faces, yaw_deg, elev_deg):
    """指定された面セットの立体を描画する."""
    for face in faces:
        draw_face(face, yaw_deg, elev_deg)
