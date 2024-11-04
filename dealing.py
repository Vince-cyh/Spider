import pandas as pd
import numpy as np
import jieba
from pyecharts.charts import Bar, Line, Pie, Map, Scatter, Page #引入柱状图、折线图、饼状图、地图
from pyecharts import options as opts


#设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 1000)

df = pd.read_csv('result.csv',header=0,encoding="utf-8-sig")
print(df.shape)         #数据大小（行、列）
print(df.head())             #数据内容,只打印了头部的前4个信息

def transform_unit(x_col):
    """
    功能：转换数值型变量的单位
    """
    # 提取数值
    s_num = df[x_col].str.extract('(\d+\.*\d*)').astype('float')
    # 提取单位
    s_unit = df[x_col].str.extract('([\u4e00-\u9fa5]+)')
    s_unit = s_unit.replace('万', 10000).replace(np.nan, 1)
    s_multiply = s_num * s_unit
    return s_multiply

# 去重
df = df.drop_duplicates()

# 删除列
df.drop('video_url', axis=1, inplace=True)

df['upload_time']=df['upload_time'].astype(str)
df['upload_time'].str.strip()
df['danmu'] = df['danmu'].astype(str)
df['danmu'].str.strip()

# 转换单位
df['view_num'] = transform_unit(x_col='view_num')
df['danmu'] = transform_unit(x_col='danmu')

# 筛选时间
df = df[(df['upload_time'] >= '2020/3/26') & (df['title'].astype('str').str.contains('粤菜'))]
#print(df.head())

#发布热度
time_num = df.upload_time.value_counts().sort_index()   #time_num中包含的是日期，及每个日期内有多少个视频发布
print(time_num)
#print(time_num.index)
#某天的播放量(https://www.cnblogs.com/zhoudayang/p/5534593.html)
time_view = df.groupby(by=['upload_time'])['view_num'].sum()      #如果需要按照列A进行分组，将同一组的列B求和
print(time_view)

# 折线图（不同的图的叠加https://[pyecharts学习笔记]——Grid并行多图、组合图、多 X/Y 轴）
line1 = Line(init_opts=opts.InitOpts(width='2000px', height='750px'))
line1.add_xaxis(time_num.index.tolist())
line1.add_yaxis('发布数量', time_num.values.tolist(),
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),    #标记最小点及最大点
                                                        opts.MarkPointItem(type_='max')]),
                # 添加第一个轴，索引为0,（默认也是0）
                yaxis_index = 0,
                color = "#d14a61",  # 系列 label 颜色，红色
               )
line1.add_yaxis('播放总量', time_view.values.tolist(),
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),
                                                        opts.MarkPointItem(type_='max')]),
                yaxis_index=1,  # 上面的折线图图默认索引为0，这里设置折线图y 轴索引为1
                color="#5793f3", # 系列 label 颜色蓝色
               )

#新加入一个y轴(索引值是1)下方是对其的详细配置
line1.extend_axis(
        yaxis=opts.AxisOpts(
            name="播放总量", # 坐标轴名称
            type_="value", # 坐标轴类型  'value': 数值轴，适用于连续数据。
            min_=0,  # 坐标轴刻度最小值
            max_=int(time_view.max()),  # 坐标轴刻度最大值
            position="right",  # 轴的位置  侧
            # 轴线配置
            axisline_opts=opts.AxisLineOpts(
                # 轴线颜色（默认黑色）
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            # 轴标签显示格式
           axislabel_opts=opts.LabelOpts(formatter="{value} c"),
        )
    )


#全局配置（全局配置中默认已经存在一个y轴了（默认索引值是0），要想更改此左侧的y轴必须更改此处的）
line1.set_global_opts(
                    yaxis_opts=opts.AxisOpts(
                                name="发布数量",
                                min_=0,
                                max_=int(time_num.max()),
                                position="left",
                                offset=80, # Y 轴相对于默认位置的偏移，在相同的 position 上有多个 Y 轴的时候有用。
                                #轴线颜色
                                axisline_opts=opts.AxisLineOpts(
                                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                                ),
                                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
                            ),
                      title_opts=opts.TitleOpts(title='粤菜视频发布热度/播放热度走势图', pos_left='5%'),#标题
                      xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),         #x轴的标签倾斜度为垂直
                    )

# 系列配置项，不显示标签（不会将折线上的每个点的值都在图中显示出来）
line1.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=3),
                      label_opts=opts.LabelOpts(is_show=False)
                     )
line1.render("line.html")


# (4)B站播放数量最高的前10个视频(x轴和y轴进行交换)
# 进行排序
top_num = df.sort_values(by='view_num',ascending=False)     #根据列view_num的值进行排序，并按照降序排列（默认是升序）
print(top_num.head(10))         #打印前十个值，降序的
top10_num=top_num.head(10).sort_values(by='view_num')   #将前10个拿出来再按照升序排列，因为后面进行条形图排列，xy轴互换时会将数最大的排在前面
print(top10_num)         #打印前十个值，升序的
columns = top10_num.reset_index()['title'].values.tolist()     #将某一列的值拿出来做为一个列表
print(columns)
data = top10_num.reset_index()['view_num'].values.tolist()     #将某一列的值拿出来做为一个列表
print(data)

#xy互换的条形图
#文字换行显示
#文字换行显示

bar2 = (
    Bar(init_opts=opts.InitOpts(width="2000px",height="700px"))        #此处通过扩大宽度，来将左侧的标题囊括过来
    .add_xaxis(columns)
    .add_yaxis("播放量", data,
               # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'),         #标注最大最小值
               #                                          opts.MarkPointItem(type_='max')]),
               )
    .reversal_axis()            #此处将x轴与y轴进行互换
    .set_global_opts(
                    title_opts=opts.TitleOpts(title="B站粤菜播放数量Top10视频",pos_left='9%'),
                    #xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate='45')),  # x轴的标签倾斜度为垂直
                    #yaxis_opts=opts.AxisOpts(axislabel_opts={"interval":"0"})   #0强制显示所有标签
                    )

    #系列配置项，将标签位置显示在右侧
    .set_series_opts( label_opts=opts.LabelOpts(position="right"))
)

bar2.render("bar2.html")
