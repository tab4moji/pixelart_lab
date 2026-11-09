"""errors.py - エラー出力専用モジュール.

目的: エラーメッセージを標準エラー出力へ集約する。
機能: report_error() で stderr に整形したメッセージを出す。

更新履歴:
  1. 2026-11-09 初版
"""

import sys


def report_error(message):
    """エラーメッセージを stderr に出力する."""
    print(f"[ERROR] {message}", file=sys.stderr)
