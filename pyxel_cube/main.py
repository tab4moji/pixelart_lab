"""main.py - 回転立方体サンプルのエントリポイント.

目的: アプリを起動し、例外を stderr に報告する。
機能: python pyxel_cube/main.py で実行(事前に uv pip install pyxel)。

更新履歴:
  1. 2026-11-09 初版
"""

import sys

from errors import report_error


def main():
    """アプリを実行し終了コードを返す."""
    status = 0
    try:
        from app import CubeApp
        CubeApp().run()
    except Exception as exc:
        report_error(f"{type(exc).__name__}: {exc}")
        status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
