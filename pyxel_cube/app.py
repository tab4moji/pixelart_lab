"""app.py - Pyxel アプリ本体.

目的: 64x64 画面で立方体を自動回転させ、見下ろし角を操作する。
機能: ↑キーで見下ろし角を増加(→90度=真上)、↓キーで減少(→0度=真横)。
      押し続けで連続変化。画面左上に角度を表示。ESCで終了。

更新履歴:
  1. 2026-11-09 初版
"""

import pyxel

from config import (BG_COLOR, DISPLAY_SCALE, ELEV_DEFAULT, ELEV_MAX,
                    ELEV_MIN, ELEV_STEP, FPS, HUD_COLOR, SCREEN_H,
                    SCREEN_W, TITLE, YAW_STEP)
from mathutil import clamp
from renderer import draw_cube


class CubeApp:
    """回転する立方体のアプリ."""

    def __init__(self):
        self.yaw = 0.0
        self.elev = ELEV_DEFAULT
        pyxel.init(SCREEN_W, SCREEN_H, title=TITLE, fps=FPS,
                   display_scale=DISPLAY_SCALE)

    def run(self):
        """メインループを開始する."""
        pyxel.run(self.update, self.draw)

    def update(self):
        """入力処理と回転角の更新."""
        if pyxel.btn(pyxel.KEY_UP):
            self.elev = clamp(self.elev + ELEV_STEP, ELEV_MIN, ELEV_MAX)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.elev = clamp(self.elev - ELEV_STEP, ELEV_MIN, ELEV_MAX)
        self.yaw = (self.yaw + YAW_STEP) % 360.0

    def draw(self):
        """1フレームを描画する."""
        pyxel.cls(BG_COLOR)
        draw_cube(self.yaw, self.elev)
        pyxel.text(1, 1, f"EL {int(self.elev):02d}", HUD_COLOR)
