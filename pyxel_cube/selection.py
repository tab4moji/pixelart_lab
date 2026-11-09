"""selection.py - 形状の選択状態と表示名.

目的: 小文字キー(単独)と大文字キー(足し込み)による形状選択の規則を、キー入力から切り離して持つ。
機能: select_shape() は選択リストを更新した新しいリストを返す。
      additive が偽なら指定した形状だけ(単独)、真なら重複しない場合のみ末尾へ追加する。
      shape_label() は左下に出す表示名を返す。単独なら従来の名前(taper は段階つき)、
      複数ならキー文字を + でつなぐ(例 C+L+E3)。

更新履歴:
  1. 2026-11-09 初版
"""

from shapes import (SHAPE_CONE, SHAPE_CUBE, SHAPE_CYLINDER, SHAPE_LABELS,
                    SHAPE_RUGBY, SHAPE_SLANT, SHAPE_TAPER, SHAPE_WEDGE)

SHAPE_TAGS = {
    SHAPE_WEDGE: "A",
    SHAPE_SLANT: "T",
    SHAPE_CYLINDER: "L",
    SHAPE_RUGBY: "R",
    SHAPE_CONE: "K",
    SHAPE_TAPER: "E",
    SHAPE_CUBE: "C",
}


def select_shape(selected, shape, additive):
    """shape を選んだ後の選択リストを返す(同じ形状は重ねない)."""
    if not additive:
        result = [shape]
    elif shape in selected:
        result = list(selected)
    else:
        result = list(selected) + [shape]
    return result


def tag_of(shape, taper_level):
    """複数表示用のキー文字を返す(taper は段階の数字つき)."""
    tag = SHAPE_TAGS[shape]
    if shape == SHAPE_TAPER and taper_level is not None:
        tag = f"{tag}{taper_level}"
    return tag


def shape_label(selected, taper_level):
    """左下に出す表示名を返す."""
    if len(selected) == 1:
        label = SHAPE_LABELS[selected[0]]
        if selected[0] == SHAPE_TAPER and taper_level is not None:
            label = f"{label} {taper_level}"
    else:
        label = "+".join(tag_of(shape, taper_level) for shape in selected)
    return label
