import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import os

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

# 设置 Seaborn 样式
sns.set_style("whitegrid")
sns.set_palette("pastel")

# 生成唯一文件名的函数
def get_unique_filename(base_name, extension, output_dir='.'):
    counter = 1
    while True:
        filename = f"{base_name}_{counter}{extension}"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1

# 连接数据库
conn = sqlite3.connect('weibo.db')
df = pd.read_sql_query("SELECT * FROM weibo", conn)
conn.close()

# 打印列名（用于调试）
print("数据库列名:", df.columns.tolist())

# 检查 '发布时间' 列是否存在
date_column = '发布时间'  # 默认列名
if date_column not in df.columns:
    # 尝试其他可能的列名
    possible_columns = ['发布日期', 'post_time', 'created_at']
    for col in possible_columns:
        if col in df.columns:
            date_column = col
            print(f"使用替代列名 '{date_column}'")
            break
    else:
        print(f"错误：未找到日期相关列。可用列：{df.columns.tolist()}")
        exit(1)

# 数据预处理：转换发布时间为日期格式
df['发布时间'] = pd.to_datetime(df[date_column])
df['日期'] = df['发布时间'].dt.date  # 提取日期部分

# 筛选数据
df = df[df['ip'].isin(['北京', '河北', '天津'])]

# 按日期统计帖子数量
daily_posts = df.groupby('日期').size().reset_index(name='帖子数量')

# 创建画布
plt.figure(figsize=(12, 6), dpi=150)

# 绘制折线图
ax = sns.lineplot(x='日期', y='帖子数量', data=daily_posts, marker='o', linewidth=2)

# 添加数据标签
for i, (date, count) in enumerate(zip(daily_posts['日期'], daily_posts['帖子数量'])):
    if i % 3 == 0:
        ax.annotate(f'{count}',
                    (date, count),
                    textcoords='offset points',
                    xytext=(0,10),
                    ha='center',
                    fontproperties=font)

# 设置标题和坐标轴标签
plt.title('每日帖子数量趋势', fontproperties=font, fontsize=16, fontweight='bold')
plt.xlabel('日期', fontproperties=font, fontsize=14)
plt.ylabel('帖子数量', fontproperties=font, fontsize=14)

# 调整刻度标签
plt.xticks(rotation=45, fontproperties=font, fontsize=10)
plt.yticks(fontproperties=font, fontsize=10)

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 移除顶部和右侧边框
sns.despine()

# 优化日期显示
plt.tight_layout()

# 获取唯一文件名并保存图片
base_filename = 'daily_posts_trend'
file_extension = '.png'
unique_filepath = get_unique_filename(base_filename, file_extension)
plt.savefig(unique_filepath, dpi=300, bbox_inches='tight')
print(f"图表已保存为: {unique_filepath}")

# 显示图表
plt.show()