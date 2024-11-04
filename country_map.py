import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

datafile = u'全国省份粤菜数量.xlsx'
data = pd.read_excel(datafile)
attr = data['省份'].tolist()
value = data['数量'].tolist()
name = []
for i in attr:
    if "省" in i:
        name.append(i.replace("省",""))
    else:
        name.append(i)
c = (
    Map(init_opts=opts.InitOpts(width="800px", height="600px"))
        .add("数量", [list(z) for z in zip(name, value)], "china")
        .set_global_opts(
        title_opts=opts.TitleOpts(title="全国粤菜店数量分布情况"),
    )
        .set_series_opts(
        label_opts=opts.LabelOpts(
        is_show=True,
        font_size=8  # 调整标签字体大小
        )
    )
        .render("全国粤菜店数量分布情况.html")
)