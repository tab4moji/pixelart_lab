# pyxel_cube 概要

64x64 の Pyxel 画面で立方体を回転させるサンプル。

## セットアップ

```bash
uv pip install pyxel
python pyxel_cube/main.py
```

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| config.py | 定数 |
| errors.py | stderr へのエラー出力 |
| mathutil.py | clamp と角度検証 |
| cube_model.py | 頂点・面・法線・色 |
| projection.py | 回転と平行投影 |
| renderer.py | 面の塗りと輪郭 |
| app.py | Pyxel アプリ本体 |
| main.py | エントリポイント |

## 更新履歴

1. 2026-11-09 初版
