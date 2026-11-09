"""shapes.py - 形状レジストリ.

目的: 形状名を描画関数 draw(yaw_deg, elev_deg) へ対応付ける。
機能: SHAPES と SHAPE_LABELS を提供する。
      立方体系はポリゴン描画(renderer.draw_shape)、円柱・ラグビーボール・円錐は
      レイキャスト描画。

更新履歴:
  1. 2026-11-09 初版(cube_model.py から分離し、円柱を追加)
  2. 2026-11-09 SHAPES を描画関数の辞書に変更し、円柱をレイキャスト化
  3. 2026-11-09 ラグビーボール(rugby)を追加
  4. 2026-11-09 円錐(cone)を追加
"""

from functools import partial

from cone_cast import draw_cone
from config import EDGE_COLOR
from cube_model import FACES_CUBE, FACES_SLANT, FACES_WEDGE, VERTICES
from cylinder_cast import draw_cylinder
from ellipsoid_cast import draw_ellipsoid
from renderer import draw_shape

SHAPE_CUBE = "cube"
SHAPE_WEDGE = "wedge"
SHAPE_SLANT = "slant"
SHAPE_CYLINDER = "cylinder"
SHAPE_RUGBY = "rugby"
SHAPE_CONE = "cone"
DEFAULT_SHAPE = SHAPE_CUBE

SHAPES = {
    SHAPE_CUBE: partial(draw_shape, (VERTICES, FACES_CUBE, EDGE_COLOR)),
    SHAPE_WEDGE: partial(draw_shape, (VERTICES, FACES_WEDGE, EDGE_COLOR)),
    SHAPE_SLANT: partial(draw_shape, (VERTICES, FACES_SLANT, EDGE_COLOR)),
    SHAPE_CYLINDER: draw_cylinder,
    SHAPE_RUGBY: draw_ellipsoid,
    SHAPE_CONE: draw_cone,
}

SHAPE_LABELS = {
    SHAPE_CUBE: "CUBE",
    SHAPE_WEDGE: "WEDGE",
    SHAPE_SLANT: "SLANT",
    SHAPE_CYLINDER: "CYL",
    SHAPE_RUGBY: "RUGBY",
    SHAPE_CONE: "CONE",
}
