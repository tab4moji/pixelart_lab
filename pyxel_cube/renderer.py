"""renderer.py - 立方体の描画.

目的: 投影済み頂点から面と辺を Pyxel で描く。
機能: 背面カリング(法線の手前成分>0の面のみ)、四角形塗り、輪郭線。
      凸立方体なので描画順の並べ替えは不要。

更新履歴:
  1. 2026-11-09 初版
"""

import pyxel

from config import EDGE_COLOR, VISIBLE_EPS
from cube_model import FACES, VERTICES
from projection import face_depth, project_point


def fill_quad(pts, color):
    """四角形を2つの三角形で塗る."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    pyxel.tri(x0, y0, x1, y1, x2, y2, color)
    pyxel.tri(x0, y0, x2, y2, x3, y3, color)


def outline_quad(pts, color):
    """四角形の輪郭線を引く."""
    for i, (x0, y0) in enumerate(pts):
        x1, y1 = pts[(i + 1) % len(pts)]
        pyxel.line(x0, y0, x1, y1, color)


def draw_face(face, yaw_deg, elev_deg):
    """カメラ側を向く面だけ描画する."""
    indices, normal, color = face
    if face_depth(normal, yaw_deg, elev_deg) > VISIBLE_EPS:
        pts = [project_point(VERTICES[i], yaw_deg, elev_deg)
               for i in indices]
        fill_quad(pts, color)
        outline_quad(pts, EDGE_COLOR)


def draw_cube(yaw_deg, elev_deg):
    """立方体全体を描画する."""
    for face in FACES:
        draw_face(face, yaw_deg, elev_deg)
