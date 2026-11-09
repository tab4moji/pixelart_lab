"""shapes.py - 形状レジストリ.

目的: 形状名を (頂点列, 面列, 輪郭色) へ対応付ける。
機能: SHAPES と SHAPE_LABELS を提供する。輪郭色が None の形状は面の色で輪郭を引く。
      立方体系は頂点を共有し、円柱は独自の頂点列を持つ。

更新履歴:
  1. 2026-11-09 初版(cube_model.py から分離し、円柱を追加)
"""

from config import EDGE_COLOR
from cube_model import FACES_CUBE, FACES_SLANT, FACES_WEDGE, VERTICES
from cylinder_model import build_cylinder

SHAPE_CUBE = "cube"
SHAPE_WEDGE = "wedge"
SHAPE_SLANT = "slant"
SHAPE_CYLINDER = "cylinder"
DEFAULT_SHAPE = SHAPE_CUBE

CYL_VERTICES, CYL_FACES = build_cylinder()

SHAPES = {
    SHAPE_CUBE: (VERTICES, FACES_CUBE, EDGE_COLOR),
    SHAPE_WEDGE: (VERTICES, FACES_WEDGE, EDGE_COLOR),
    SHAPE_SLANT: (VERTICES, FACES_SLANT, EDGE_COLOR),
    SHAPE_CYLINDER: (CYL_VERTICES, CYL_FACES, None),
}

SHAPE_LABELS = {
    SHAPE_CUBE: "CUBE",
    SHAPE_WEDGE: "WEDGE",
    SHAPE_SLANT: "SLANT",
    SHAPE_CYLINDER: "CYL",
}
