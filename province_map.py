import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts

datafile = u'全国城市粤菜数量.xlsx'
data = pd.read_excel(datafile)
city = data['城市'].tolist()
values2 = data['数量'].tolist()

name = []
value = []
flag = 0
for i in range(0, len(city)):
    name.append(city[i])
    value.append(int(values2[i]))

# 自定义各个区间的取值范围和颜色
pieces = [
    {"min": 0, "max": 500, "label": "0-10", "color": "#eff5fb"},
    {"min": 501, "max": 1000, "label": "11-50", "color": "#cce0ff"},
    {"min": 1001, "max": 3000, "label": "51-100", "color": "#94c6e8"},
    {"min": 3001, "max": 8000, "label": "101-500", "color": "#62a9e8"},
    {"min": 8001, "max": 15000, "label": "501-1000", "color": "#0077cc"},
]

c = (
    Map(init_opts=opts.InitOpts(width="1500px", height="800px"))
    .add("广东粤菜数量分布", [list(z) for z in zip(name, value)], "广东")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="广东粤菜数量分布"), visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,  # 是否为分段型
            pieces=pieces,  # 自定义各个区间的取值范围和颜色
            orient="horizontal",  # 显示的方向，水平或垂直
            pos_bottom="10%",  # 位置设置，可以是百分比或像素值
            type_="log"
        )
    )
    .render("广东粤菜数量分布.html")
)
