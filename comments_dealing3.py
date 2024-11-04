import jieba
import pandas as pd
from wordcloud import WordCloud
from pyecharts.charts import WordCould
df = pd.read_csv('bilibili评论数据.csv')
print(df.head())
# 导入停词文件
stopword = open('stopwords.txt', encoding='utf8').read().split('\n')
# 进行分词
data = jieba.lcut(''.join(df.content))
# 统计词频
word = {}
for i in data:
    if i not in stopword:
        word[i] = word.get(i, 0) + 1
# 绘制词云图
wc = WordCloud()
wc.add('', word.items(), shape='triangle')
wc.render('Ciyun.html')