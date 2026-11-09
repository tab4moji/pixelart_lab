"""app.py - Pyxel アプリ本体.

目的: 64x64 画面で立体を自動回転させ、見下ろし角と形状を操作する。
機能: ↑キーで見下ろし角を増加(→90度=真上)、↓キーで減少(→0度=真横)。
      A: 対角線切断ブロック(wedge)、T: 側面の対角線切断ブロック(slant)、
      L: 横向き円柱(cylinder)、R: 横向きラグビーボール(rugby)、
      K: 横向き円錐(cone)、E: 先細りラグビーボール(taper)、
      C: 通常の立方体。Q または ESC で終了。
      左上に角度、左下に形状名を表示。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 Q終了、A/Cによる形状切替を追加
  3. 2026-11-09 Tキー(slant)を追加し、形状キーをテーブル化
  4. 2026-11-09 Lキー(横向き円柱)を追加し、形状定義を shapes.py へ移行
  5. 2026-11-09 SHAPES が描画関数を返す形式に合わせて draw を変更
  6. 2026-11-09 Rキー(ラグビーボール)を追加
  7. 2026-11-09 Kキー(円錐)を追加
  8. 2026-11-09 Eキー(先細りラグビーボール)を追加
"""

import pyxel

from config import (BG_COLOR, DISPLAY_SCALE, ELEV_DEFAULT, ELEV_MAX,
                    ELEV_MIN, ELEV_STEP, FPS, HUD_COLOR, SCREEN_H,
                    SCREEN_W, TITLE, YAW_STEP)
from mathutil import clamp
from shapes import (DEFAULT_SHAPE, SHAPE_CONE, SHAPE_CUBE, SHAPE_CYLINDER,
                    SHAPE_LABELS, SHAPE_RUGBY, SHAPE_SLANT, SHAPE_TAPER,
                    SHAPE_WEDGE, SHAPES)

SHAPE_KEYS = (
    (pyxel.KEY_A, SHAPE_WEDGE),
    (pyxel.KEY_T, SHAPE_SLANT),
    (pyxel.KEY_L, SHAPE_CYLINDER),
    (pyxel.KEY_R, SHAPE_RUGBY),
    (pyxel.KEY_K, SHAPE_CONE),
    (pyxel.KEY_E, SHAPE_TAPER),
    (pyxel.KEY_C, SHAPE_CUBE),
)


class CubeApp:
    """回転する立体のアプリ."""

    def __init__(self):
        self.yaw = 0.0
        self.elev = ELEV_DEFAULT
        self.shape = DEFAULT_SHAPE
        pyxel.init(SCREEN_W, SCREEN_H, title=TITLE, fps=FPS,
                   display_scale=DISPLAY_SCALE)

    def run(self):
        """メインループを開始する."""
        pyxel.run(self.update, self.draw)

    def handle_shape_keys(self):
        """A/T/L/R/K/E/C キーで形状を切り替える."""
        for key, shape in SHAPE_KEYS:
            if pyxel.btnp(key):
                self.shape = shape

    def handle_elev_keys(self):
        """↑↓キーで見下ろし角を変更する."""
        if pyxel.btn(pyxel.KEY_UP):
            self.elev = clamp(self.elev + ELEV_STEP, ELEV_MIN, ELEV_MAX)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.elev = clamp(self.elev - ELEV_STEP, ELEV_MIN, ELEV_MAX)

    def update(self):
        """入力処理と回転角の更新."""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.handle_shape_keys()
        self.handle_elev_keys()
        self.yaw = (self.yaw + YAW_STEP) % 360.0

    def draw(self):
        """1フレームを描画する."""
        pyxel.cls(BG_COLOR)
        SHAPES[self.shape](self.yaw, self.elev)
        pyxel.text(1, 1, f"EL {int(self.elev):02d}", HUD_COLOR)
        pyxel.text(1, 58, SHAPE_LABELS[self.shape], HUD_COLOR)
