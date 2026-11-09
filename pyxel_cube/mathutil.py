"""mathutil.py - 数値ユーティリティ.

目的: 範囲制限と引数検証を提供する。
機能: clamp() と validate_elevation()。不正値は例外で通知する。

更新履歴:
  1. 2026-11-09 初版
"""

from config import ELEV_MAX, ELEV_MIN


def clamp(value, low, high):
    """value を [low, high] に収めて返す."""
    if low > high:
        raise ValueError(f"low({low}) > high({high})")
    result = max(low, min(high, value))
    return result


def validate_elevation(elev_deg):
    """見下ろし角が 0〜90 度であることを検証して返す."""
    if not ELEV_MIN <= elev_deg <= ELEV_MAX:
        raise ValueError(f"elevation out of range: {elev_deg}")
    result = elev_deg
    return result
