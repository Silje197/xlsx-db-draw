import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import os
from matplotlib.dates import DateFormatter, DayLocator
import numpy as np

# 查找系统中可用的中文字体
import matplotlib.font_manager as fm

fonts = fm.findSystemFonts()
chinese_fonts = [f for f in fonts if 'hei' in f.lower() or 'microsoft' in f.lower() or 'sim' in f.lower()]
print("可用中文字体:", chinese_fonts)

# 指定中文字体
try:
    font_path = r"C:\Windows\Fonts\simhei.ttf"
    font = FontProperties(fname=font_path)
except:
    print("未找到指定字体，使用默认设置")
    font = None

# 设置 Seaborn 样式和配色
sns.set_style("whitegrid")
plt.rcParams["grid.linestyle"] = "--"  # 虚线网格
sns.set_palette("pastel")  # pastel配色方案


# 生成唯一文件名的函数
def get_unique_filename(base_name, extension, output_dir='.'):
    counter = 1
    while True:
        filename = f"{base_name}_{counter}{extension}"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1


# 读取Excel文件并预处理
df = pd.read_excel('weibo_bosonnlp_sentiment.xlsx')
date_column = 'created_at'  # 日期列名
region_column = 'ip'  # 地区列名

df[date_column] = pd.to_datetime(df[date_column])
df['日期'] = df[date_column].dt.date  # 提取日期部分（不含时间）

# 统计数据
daily_posts_by_region = df.groupby(['日期', region_column]).size().reset_index(name='帖子数量')
daily_total_posts = daily_posts_by_region.groupby('日期')['帖子数量'].sum().reset_index()
regions = daily_posts_by_region.groupby(region_column)['帖子数量'].sum().sort_values(ascending=False).index.tolist()

# 创建画布
plt.figure(figsize=(14, 7), dpi=150)
unique_dates = sorted(daily_posts_by_region['日期'].unique())
num_dates = len(unique_dates)
num_regions = len(regions)

# 设置柱状图参数
bar_width = 0.8  # 所有柱子的总宽度比例
single_width = bar_width / num_regions  # 单个柱子宽度

# 绘制各地区柱状图（使用数值索引）
for i, region in enumerate(regions):
    region_data = daily_posts_by_region[daily_posts_by_region[region_column] == region]

    # 创建该地区的x轴位置（数值索引）
    x_positions = np.arange(num_dates) + i * single_width

    # 确保数据包含所有日期
    region_values = []
    for date in unique_dates:
        date_data = region_data[region_data['日期'] == date]
        region_values.append(date_data['帖子数量'].values[0] if len(date_data) > 0 else 0)

    # 绘制柱子
    plt.bar(
        x_positions,
        region_values,
        width=single_width,
        alpha=0.8,
        label=region,
        edgecolor='white',
        align='edge'  # 边缘对齐，确保柱子间距均匀
    )

    # 添加柱子顶部数值
    for pos, value in zip(x_positions, region_values):
        if value > 0:
            plt.text(
                pos + single_width / 2,  # 文字居中
                value + 0.5,
                f"{int(value)}",
                ha='center',
                va='bottom',
                fontproperties=font,
                fontsize=8
            )

# 绘制总帖子数折线图（使用数值索引）
plt.plot(
    np.arange(num_dates) + bar_width / 2,  # 折线居中
    daily_total_posts['帖子数量'],
    color='red',
    marker='o',
    markersize=6,
    linewidth=2,
    label='总帖子数'
)

# 添加折线图节点数值
for x, y in zip(np.arange(num_dates) + bar_width / 2, daily_total_posts['帖子数量']):
    plt.text(
        x,
        y + 3,
        f"{int(y)}",
        ha='center',
        va='bottom',
        fontproperties=font,
        fontsize=9,
        color='black'
    )

# 设置x轴刻度和标签为日期
plt.xticks(
    np.arange(num_dates) + bar_width / 2,  # 刻度居中
    [date.strftime('%Y-%m-%d') for date in unique_dates],
    rotation=45,
    ha='right',
    fontproperties=font
)

# 图表标签和标题
plt.title('每日各地区帖子数量分布', fontproperties=font, fontsize=16, fontweight='bold')
plt.xlabel('日期', fontproperties=font, fontsize=14)
plt.ylabel('帖子数量', fontproperties=font, fontsize=14)
plt.yticks(fontproperties=font)

# 调整图例顺序（总帖子数放最后）
handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[:-1] + [handles[-1]]  # 总帖子数移到最后
labels = labels[:-1] + [labels[-1]]

# 添加图例
plt.legend(
    handles, labels,
    prop=font,
    title_fontproperties=font,
    title="地区",
    loc="upper left"
)

# 移除顶部和右侧边框
sns.despine()

# 优化布局并保存
plt.tight_layout()
unique_filepath = get_unique_filename('daily_posts_comparison', '.png')
plt.savefig(unique_filepath, dpi=300, bbox_inches='tight')
print(f"图表已保存为: {unique_filepath}")

# 显示图表
plt.show()