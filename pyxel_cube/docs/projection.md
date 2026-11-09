# 投影の数式

平行投影。座標は Y 上、回転角 yaw、見下ろし角 e。

## Y軸回転

```
x' = x*cos(yaw) + z*sin(yaw)
z' = -x*sin(yaw) + z*cos(yaw)
```

## 見下ろし角

```
up    = y*cos(e) - z'*sin(e)
depth = y*sin(e) + z'*cos(e)
```

- e=0 なら up=y で真横から見る。
- e=90 なら up=-z' で真上から見る(奥が画面上)。

## 画面座標

```
sx = CENTER_X + x'*SCALE
sy = CENTER_Y - up*SCALE
```

## 背面カリング

面の法線に同じ変換をかけ、depth > 0 の面だけ描く。
立方体は凸なので面同士は重ならず、ソート不要。

## 更新履歴

1. 2026-11-09 初版
