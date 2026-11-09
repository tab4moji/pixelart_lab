"""config.py - 回転立方体サンプルの定数定義.

目的: 画面サイズ・カメラ・描画色などの定数を一箇所に集約する。
機能: 他モジュールから参照される読み取り専用の定数を提供する。

更新履歴:
  1. 2026-11-09 初版
"""

SCREEN_W = 64
SCREEN_H = 64
FPS = 30
DISPLAY_SCALE = 8
TITLE = "pyxel cube"

CENTER_X = 32
CENTER_Y = 36
SCALE = 14.0

ELEV_MIN = 0.0
ELEV_MAX = 90.0
ELEV_DEFAULT = 30.0
ELEV_STEP = 1.0
YAW_STEP = 2.0

VISIBLE_EPS = 1e-6

BG_COLOR = 0
EDGE_COLOR = 7
HUD_COLOR = 7
