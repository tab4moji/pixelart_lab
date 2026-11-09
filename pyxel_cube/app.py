"""app.py - Pyxel アプリ本体.

目的: 64x64 画面で立体を自動回転させ、見下ろし角と形状を操作する。
機能: ↑キーで見下ろし角を増加(→90度=真上)、↓キーで減少(→0度=真横)。
      形状キー: A=wedge、T=slant、L=円柱、R=ラグビーボール、K=円錐、
      E=先細りラグビーボール、C=立方体。Q または ESC で終了。
      小文字(Shift なし)は、その形状だけを単独で表示する。
      大文字(Shift あり)は、いま表示中の形状へその形状を足す(同じ形状は重ねない)。
      複数のときは Z バッファで合成して表示する。
      taper が表示中のときだけ 1〜5 キーで小球の大きさを変える。
      1=点、2=大球の1/4、3=1/2、4=3/4、5=大球と1:1。
      左上に角度、左下に形状名(複数は C+L+E3 のようにキー文字)を表示。

更新履歴:
  1. 2026-11-09 初版
  2. 2026-11-09 Q終了、A/Cによる形状切替を追加
  3. 2026-11-09 Tキー(slant)を追加し、形状キーをテーブル化
  4. 2026-11-09 Lキー(横向き円柱)を追加し、形状定義を shapes.py へ移行
  5. 2026-11-09 SHAPES が描画関数を返す形式に合わせて draw を変更
  6. 2026-11-09 Rキー(ラグビーボール)を追加
  7. 2026-11-09 Kキー(円錐)を追加
  8. 2026-11-09 Eキー(先細りラグビーボール)を追加
  9. 2026-11-09 taper 専用の 1〜5 キー(小球の大きさ)を追加
  10. 2026-11-09 大文字(Shift)で形状を足し込み、Z バッファで合成する機能を追加
"""

import pyxel

from composite import draw_composite
from config import (BG_COLOR, DISPLAY_SCALE, ELEV_DEFAULT, ELEV_MAX,
                    ELEV_MIN, ELEV_STEP, FPS, HUD_COLOR, SCREEN_H,
                    SCREEN_W, TITLE, YAW_STEP)
from mathutil import clamp
from selection import select_shape, shape_label
from shapes import (DEFAULT_SHAPE, SHAPE_CONE, SHAPE_CUBE, SHAPE_CYLINDER,
                    SHAPE_RUGBY, SHAPE_SLANT, SHAPE_TAPER, SHAPE_WEDGE,
                    SHAPES)
from tapered_cast import draw_tapered
from tapered_model import DEFAULT_RATIO, ratio_from_level

SHAPE_KEYS = (
    (pyxel.KEY_A, SHAPE_WEDGE),
    (pyxel.KEY_T, SHAPE_SLANT),
    (pyxel.KEY_L, SHAPE_CYLINDER),
    (pyxel.KEY_R, SHAPE_RUGBY),
    (pyxel.KEY_K, SHAPE_CONE),
    (pyxel.KEY_E, SHAPE_TAPER),
    (pyxel.KEY_C, SHAPE_CUBE),
)

TAPER_KEYS = (
    (pyxel.KEY_1, 1),
    (pyxel.KEY_2, 2),
    (pyxel.KEY_3, 3),
    (pyxel.KEY_4, 4),
    (pyxel.KEY_5, 5),
)


class CubeApp:
    """回転する立体のアプリ."""

    def __init__(self):
        self.yaw = 0.0
        self.elev = ELEV_DEFAULT
        self.selected = [DEFAULT_SHAPE]
        self.taper_level = None
        self.taper_ratio = DEFAULT_RATIO
        pyxel.init(SCREEN_W, SCREEN_H, title=TITLE, fps=FPS,
                   display_scale=DISPLAY_SCALE)

    def run(self):
        """メインループを開始する."""
        pyxel.run(self.update, self.draw)

    def handle_shape_keys(self):
        """形状キーを処理する。Shift ありなら足し込み、なしなら単独."""
        additive = pyxel.btn(pyxel.KEY_SHIFT)
        for key, shape in SHAPE_KEYS:
            if pyxel.btnp(key):
                self.selected = select_shape(self.selected, shape, additive)

    def handle_taper_keys(self):
        """taper が表示中のときだけ 1〜5 キーで小球の大きさを変える."""
        if SHAPE_TAPER in self.selected:
            for key, level in TAPER_KEYS:
                if pyxel.btnp(key):
                    self.taper_level = level
                    self.taper_ratio = ratio_from_level(level)

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
        self.handle_taper_keys()
        self.handle_elev_keys()
        self.yaw = (self.yaw + YAW_STEP) % 360.0

    def draw_selected(self):
        """単独は従来の描画、複数は Z バッファ合成で描く."""
        if len(self.selected) > 1:
            draw_composite(self.yaw, self.elev, self.selected,
                           self.taper_ratio)
        elif self.selected[0] == SHAPE_TAPER:
            draw_tapered(self.yaw, self.elev, self.taper_ratio)
        else:
            SHAPES[self.selected[0]](self.yaw, self.elev)

    def draw(self):
        """1フレームを描画する."""
        pyxel.cls(BG_COLOR)
        self.draw_selected()
        pyxel.text(1, 1, f"EL {int(self.elev):02d}", HUD_COLOR)
        pyxel.text(1, 58, shape_label(self.selected, self.taper_level),
                   HUD_COLOR)
