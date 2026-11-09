"""shapes.py - 形状レジストリ.

目的: 形状名を描画関数 draw(yaw_deg, elev_deg) へ対応付ける。
機能: SHAPES と SHAPE_LABELS を提供する。
      立方体系はポリゴン描画(renderer.draw_shape)、円柱はレイキャスト描画。

更新履歴:
  1. 2026-11-09 初版(cube_model.py から分離し、円柱を追加)
  2. 2026-11-09 SHAPES を描画関数の辞書に変更し、円柱をレイキャスト化
"""

from functools import partial

from config import EDGE_COLOR
from cube_model import FACES_CUBE, FACES_SLANT, FACES_WEDGE, VERTICES
from cylinder_cast import draw_cylinder
from renderer import draw_shape

SHAPE_CUBE = "cube"
SHAPE_WEDGE = "wedge"
SHAPE_SLANT = "slant"
SHAPE_CYLINDER = "cylinder"
DEFAULT_SHAPE = SHAPE_CUBE

SHAPES = {
    SHAPE_CUBE: partial(draw_shape, (VERTICES, FACES_CUBE, EDGE_COLOR)),
    SHAPE_WEDGE: partial(draw_shape, (VERTICES, FACES_WEDGE, EDGE_COLOR)),
    SHAPE_SLANT: partial(draw_shape, (VERTICES, FACES_SLANT, EDGE_COLOR)),
    SHAPE_CYLINDER: draw_cylinder,
}

SHAPE_LABELS = {
    SHAPE_CUBE: "CUBE",
    SHAPE_WEDGE: "WEDGE",
    SHAPE_SLANT: "SLANT",
    SHAPE_CYLINDER: "CYL",
}
