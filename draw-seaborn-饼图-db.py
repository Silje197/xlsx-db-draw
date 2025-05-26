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
sns.set_style("white")  # 简洁背景

# 生成唯一文件名的函数
def get_unique_filename(base_name, extension, output_dir='.'):
    counter = 1
    while True:
        filename = f"{base_name}_{counter}{extension}"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1

# 读取Excel文件
df = pd.read_excel('weibo_bosonnlp_sentiment.xlsx')

# 统计各地区帖子数量并排序
region_counts = df['ip'].value_counts().reset_index()
region_counts.columns = ['地区', '帖子数量']
region_counts = region_counts.sort_values('帖子数量', ascending=False)  # 按帖子数量降序排列

# 计算百分比
total_posts = region_counts['帖子数量'].sum()
region_counts['百分比'] = region_counts['帖子数量'] / total_posts * 100

# 创建画布
plt.figure(figsize=(8, 5), dpi=150)

# 使用 Seaborn 调色板
colors = sns.color_palette('pastel')[:len(region_counts)]  # 根据地区数量动态调整颜色

# 绘制饼图（移除labels参数，添加图例）
patches, texts, autotexts = plt.pie(
    region_counts['帖子数量'],
    colors=colors,
    autopct='%1.1f%%',  # 显示百分比
    startangle=90,      # 从垂直方向开始
    counterclock=False, # 顺时针排列
    textprops={'fontproperties': font, 'fontsize': 12},  # 设置中文字体
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}  # 添加白色边框
)

# 添加图例（使用地区名，恢复原始位置和边框）
plt.legend(
    patches,
    region_counts['地区'],
    title="地区",
    title_fontproperties=font,  # 设置图例标题字体
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),  # 恢复原始图例位置
    prop=font,  # 设置图例文本字体
    frameon=True,  # 恢复图例边框
    edgecolor='gray',  # 设置边框颜色
    framealpha=0.8  # 设置边框透明度
)

# 设置标题
plt.title('各地区帖子数量占比', fontproperties=font, fontsize=16, fontweight='bold')

# 确保饼图是圆形
plt.axis('equal')

# 优化布局
plt.tight_layout()

# 获取唯一文件名并保存图片
base_filename = 'region_posts_pie_chart'
file_extension = '.png'
unique_filepath = get_unique_filename(base_filename, file_extension)
plt.savefig(unique_filepath, dpi=300, bbox_inches='tight')
print(f"图表已保存为: {unique_filepath}")

# 显示图表
plt.show()