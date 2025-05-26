import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType

# 读取数据并统计各省帖子总量
df = pd.read_excel('weibo_bosonnlp_sentiment.xlsx')
region_column = 'ip'  # 地区列名

# 统计各省帖子数量
province_posts = df.groupby(region_column).size().reset_index(name='帖子数量')

# 确保省份名称与 pyecharts 地图匹配（部分名称需转换）
province_mapping = {
    '北京': '北京市', '天津': '天津市', '河北': '河北省', '山西': '山西省',
    '内蒙古': '内蒙古自治区', '辽宁': '辽宁省', '吉林': '吉林省', '黑龙江': '黑龙江省',
    '上海': '上海市', '江苏': '江苏省', '浙江': '浙江省', '安徽': '安徽省',
    '福建': '福建省', '江西': '江西省', '山东': '山东省', '河南': '河南省',
    '湖北': '湖北省', '湖南': '湖南省', '广东': '广东省', '广西': '广西壮族自治区',
    '海南': '海南省', '重庆': '重庆市', '四川': '四川省', '贵州': '贵州省',
    '云南': '云南省', '西藏': '西藏自治区', '陕西': '陕西省', '甘肃': '甘肃省',
    '青海': '青海省', '宁夏': '宁夏回族自治区', '新疆': '新疆维吾尔自治区',
    '台湾': '台湾省', '香港': '香港特别行政区', '澳门': '澳门特别行政区'
}

# 转换省份名称
province_posts['省份'] = province_posts[region_column].map(province_mapping)
# 过滤掉无法匹配的地区
province_posts = province_posts.dropna(subset=['省份'])

# 准备地图数据
map_data = [list(z) for z in zip(province_posts['省份'], province_posts['帖子数量'])]

# 创建地图
(
    Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="600px"))
    .add("帖子数量", map_data, "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各省帖子数量热力图"),
        visualmap_opts=opts.VisualMapOpts(
            max_=province_posts['帖子数量'].max(),
            range_text=["高", "低"],
            is_piecewise=True,  # 分段显示
            pieces=[
                {"max": 999999, "min": 10000, "label": "10000+"},
                {"max": 9999, "min": 1000, "label": "1000-9999"},
                {"max": 999, "min": 100, "label": "100-999"},
                {"max": 99, "min": 10, "label": "10-99"},
                {"max": 9, "min": 0, "label": "0-9"}
            ],
        ),
        toolbox_opts=opts.ToolboxOpts(is_show=True)  # 显示工具栏
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True)  # 显示省份名称
    )
    .render("province_posts_heatmap.html")  # 保存为 HTML 文件
)

print("热力图已保存为 province_posts_heatmap.html，请用浏览器打开查看")