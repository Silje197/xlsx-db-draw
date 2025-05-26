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
    # Windows 系统
    font_path = r"C:\Windows\Fonts\simhei.ttf"
    # macOS 系统
    # font_path = "/System/Library/Fonts/PingFang.ttc"
    font = FontProperties(fname=font_path)
except:
    print("未找到指定字体，使用默认设置")
    font = None

# 设置 Seaborn 样式
sns.set_style("whitegrid")
# 数据探索：优先用 darkgrid 或 whitegrid，网格线帮助定位数据点。
# 演示/出版：white 或 ticks，简洁无干扰。
# 高对比度场景：用 dark 风格。
sns.set_palette("pastel")


# 生成唯一文件名的函数
def get_unique_filename(base_name, extension, output_dir='.'):
    """生成带编号的唯一文件名，避免覆盖已有文件"""
    counter = 1
    while True:
        # 生成带编号的文件名
        filename = f"{base_name}_{counter}{extension}"
        filepath = os.path.join(output_dir, filename)

        # 检查文件是否存在
        if not os.path.exists(filepath):
            return filepath

        # 若存在，增加计数器
        counter += 1


# 连接数据库
conn = sqlite3.connect('weibo.db')
df = pd.read_sql_query("SELECT * FROM weibo", conn)
conn.close()

# 筛选数据
df = df[df['ip'].isin(['北京', '河北', '天津'])]

# 统计各地区数据量
region_counts = df['ip'].value_counts().reset_index()
region_counts.columns = ['地区', '数据量']

# 创建画布
plt.figure(figsize=(8, 5), dpi=150)

# 绘制柱状图
ax = sns.barplot(x='地区', y='数据量', data=region_counts)

# 添加数据标签
for p in ax.patches:
    ax.annotate(f'{p.get_height()}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                fontsize=10, color='black',
                fontproperties=font,
                xytext=(0, 5), textcoords='offset points')

# 设置标题和坐标轴标签
plt.title('各地区数据量统计', fontproperties=font, fontsize=14, fontweight='bold')
plt.xlabel('地区', fontproperties=font, fontsize=12)
plt.ylabel('数据量', fontproperties=font, fontsize=12)

# 调整刻度标签
plt.xticks(fontproperties=font, fontsize=10)
plt.yticks(fontsize=10)

# 调整 Y 轴范围
plt.ylim(0, region_counts['数据量'].max() * 1.1)

# 移除顶部和右侧边框
sns.despine()

# 获取唯一文件名并保存图片
base_filename = 'region_counts'
file_extension = '.png'
unique_filepath = get_unique_filename(base_filename, file_extension)
plt.savefig(unique_filepath, dpi=300, bbox_inches='tight')
print(f"图表已保存为: {unique_filepath}")

# 显示图表
plt.show()