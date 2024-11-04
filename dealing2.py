import pandas as pd
import numpy as np
import jieba
from pyecharts.charts import Line
from pyecharts import options as opts

# 设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 1000)

df = pd.read_csv('result.csv', header=0, encoding="utf-8-sig")

# 数据清洗
df = df.drop_duplicates()
df.drop('video_url', axis=1, inplace=True)

df['upload_time'] = pd.to_datetime(df['upload_time'], format='%Y/%m/%d')
df['upload_year'] = df['upload_time'].dt.year

df['upload_time']=df['upload_time'].astype(str)
df['upload_time'].str.strip()
df['danmu'] = df['danmu'].astype(str)
df['danmu'].str.strip()

# 转换单位
def transform_unit(x_col):
    s_num = df[x_col].str.extract('(\d+\.*\d*)').astype('float')
    s_unit = df[x_col].str.extract('([\u4e00-\u9fa5]+)')
    s_unit = s_unit.replace('万', 10000).replace(np.nan, 1)
    s_multiply = s_num * s_unit
    return s_multiply

df['view_num'] = transform_unit(x_col='view_num')
df['danmu'] = transform_unit(x_col='danmu')

# 筛选时间
df = df[(df['upload_time'] >= '2018/01/01') & (df['title'].astype('str').str.contains('粤菜'))]

# 按年份分组并统计发布数量和播放总量
yearly_stats = df.groupby(by=['upload_year'])[['upload_time', 'view_num']].agg({'upload_time': 'count', 'view_num': 'sum'})

# 生成折线图
line1 = Line(init_opts=opts.InitOpts(width='2000px', height='750px'))
line1.add_xaxis(yearly_stats.index.tolist())
line1.add_yaxis('发布数量', yearly_stats['upload_time'].tolist(), markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]), yaxis_index=0, color="#d14a61")
line1.add_yaxis('播放总量', yearly_stats['view_num'].tolist(), markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]), yaxis_index=1, color="#5793f3")

# 添加第二个y轴
line1.extend_axis(
    yaxis=opts.AxisOpts(
        name="播放总量",
        type_="value",
        min_=0,
        max_=int(yearly_stats['view_num'].max()) + 5000000,
        position="right",
        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
        axislabel_opts=opts.LabelOpts(formatter="{value} c"),
    )
)

# 全局配置
line1.set_global_opts(
    yaxis_opts=opts.AxisOpts(
        name="发布数量",
        min_=0,
        max_=int(yearly_stats['upload_time'].max()),
        position="left",
        offset=80,
        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
        axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
    ),
    title_opts=opts.TitleOpts(title='近5年粤菜视频发布热度/播放热度走势图', pos_left='5%'),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),
)

# 系列配置项
line1.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=3), label_opts=opts.LabelOpts(is_show=False))

print(yearly_stats)

# 生成折线图
line1.render("line.html")
