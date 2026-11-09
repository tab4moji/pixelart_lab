"""samplers.py - 形状ごとの Z合成用サンプラ.

目的: 形状名から、画素ごとに (深度 t, 色, 面ID) を返す sampler を作る。
機能: build_entries() が (sampler, 走査範囲, 輪郭フラグ) のリストを返す。
      sampler(px, py, x_pos, up) の形に揃えてあり、view や形状パラメータは
      フレームごとに束縛する(taper は小球の比率 ratio を使う)。
      立方体系は輪郭フラグ True(白い輪郭線を引く)、他は False。

更新履歴:
  1. 2026-11-09 初版
"""

import math
from functools import partial

import cone_cast
import cylinder_cast
import ellipsoid_cast
import tapered_cast
from config import SCALE
from cube_model import FACES_CUBE, FACES_SLANT, FACES_WEDGE, VERTICES
from poly_cast import build_planes, make_poly_sampler
from shapes import (SHAPE_CONE, SHAPE_CUBE, SHAPE_CYLINDER, SHAPE_RUGBY,
                    SHAPE_SLANT, SHAPE_TAPER, SHAPE_WEDGE)
from tapered_model import make_geometry

POLY_EXTENT = int(math.sqrt(3.0) * SCALE) + 2

PLANES = {
    SHAPE_CUBE: build_planes(VERTICES, FACES_CUBE),
    SHAPE_WEDGE: build_planes(VERTICES, FACES_WEDGE),
    SHAPE_SLANT: build_planes(VERTICES, FACES_SLANT),
}


def poly_entry(name, view):
    """立方体系の (sampler, 範囲, 輪郭フラグ)."""
    result = (make_poly_sampler(PLANES[name], view), POLY_EXTENT, True)
    return result


def cylinder_entry(view):
    """円柱の (sampler, 範囲, 輪郭フラグ)."""
    result = (partial(cylinder_cast.sample_pixel, view=view),
              cylinder_cast.EXTENT, False)
    return result


def rugby_entry(view):
    """ラグビーボールの (sampler, 範囲, 輪郭フラグ)."""
    result = (partial(ellipsoid_cast.sample_pixel, view=view),
              ellipsoid_cast.EXTENT, False)
    return result


def cone_entry(view):
    """円錐の (sampler, 範囲, 輪郭フラグ)."""
    result = (partial(cone_cast.sample_pixel, view=view),
              cone_cast.EXTENT, False)
    return result


def taper_entry(view, ratio):
    """先細りラグビーボールの (sampler, 範囲, 輪郭フラグ)."""
    geo = make_geometry(ratio)
    result = (partial(tapered_cast.sample_pixel, view=view, geo=geo),
              int(geo.bound * SCALE) + 2, False)
    return result


def build_entry(name, view, ratio):
    """形状名から (sampler, 範囲, 輪郭フラグ) を作る。未知の名前は ValueError."""
    if name in PLANES:
        result = poly_entry(name, view)
    elif name == SHAPE_CYLINDER:
        result = cylinder_entry(view)
    elif name == SHAPE_RUGBY:
        result = rugby_entry(view)
    elif name == SHAPE_CONE:
        result = cone_entry(view)
    elif name == SHAPE_TAPER:
        result = taper_entry(view, ratio)
    else:
        raise ValueError(f"unknown shape: {name}")
    return result


def build_entries(names, view, ratio):
    """形状名のリストから entry のリストを作る."""
    return [build_entry(name, view, ratio) for name in names]
