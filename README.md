# 图表绘制

## 主要工具

- Matplotlib：Python自带，轻量
- Seaborn：美观
- Plotly：生成HTML网页，可交互

## 关于Seaborn

### 风格选择

```python
sns.set_style("whitegrid")
```

数据探索：优先用 darkgrid 或 whitegrid，网格线帮助定位数据点。

演示/出版：white 或 ticks，简洁无干扰。

高对比度场景：用 dark 风格。

### 配色方案

```python
sns.set_palette("pastel")
```

Seaborn有六种matplotlib调色板的变体：`deep`，`muted`，`pastel`，`bright`，`dark`，`colorblind`。

![attachment:2f1e85e4-26d0-46af-a90b-73b2d2b0bf1b:image.png](https://pica.zhimg.com/v2-6e9db10ef2f01276f62d56839822cfb0_1440w.jpg)

### 高级配色（自定义）

[matplotlib、seaborn颜色、调色板、调色盘。 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/572193380)
