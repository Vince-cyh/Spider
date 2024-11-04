import pandas as pd
import jieba
from collections import Counter
from pyecharts.charts import Bar
from pyecharts import options as opts

# 读取数据
data = pd.read_csv('bili_danmu2.csv', header=0, encoding="utf-8-sig")
text = ''.join(data['comments'])
words = list(jieba.cut(text))

# 去除停用词（可以根据需要修改停用词表）
stop_words = [x.strip() for x in open('stopwords.txt', encoding="utf-8")]
filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]

# 计算词频
word_counts = Counter(filtered_words)

# 输出“广州”一词的出现次数
guangzhou_count = word_counts.get('广州', 0)  # 获取“广州”一词的出现次数，如果不存在则返回0
print("“广州”一词出现的次数：", guangzhou_count)

top_words = word_counts.most_common(10)  # 获取词频最高的前十个词

# 提取词和词频
words, counts = zip(*top_words)

# 创建柱状图
bar = (
    Bar()
    .add_xaxis(list(words))
    .add_yaxis(
        "词频",
        list(counts),
        label_opts=opts.LabelOpts(position="inside", font_size=16),
        itemstyle_opts=opts.ItemStyleOpts(
            color="#0077cc",  # 设置柱形颜色
            border_color="#0077cc",  # 设置边框颜色
            border_width=1,  # 设置边框宽度
            border_radius=[20, 20, 0, 0]  # 设置柱形顶端为半圆形状
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="词频最高的前十个词"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45, font_size=15)),
    )
)

# 保存柱状图到danmu_line.html文件中
bar.render("danmu_line.html")
