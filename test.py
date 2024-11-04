import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('bili_danmu2.csv', header=0, encoding="utf-8-sig")

# 读取停止词
with open('stopwords.txt', 'r', encoding="utf-8") as file:
    stop_words = set([line.strip() for line in file.readlines()])

# 分词并统计词频
word_freq = {}
for comment in data['comments']:
    words = jieba.cut(comment)
    for word in words:
        if len(word) > 1 and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

# 获取频率最高的前十个词
top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

# 可视化最高频的前十个词
wordcloud_data = {word: freq for word, freq in top_words}
wordcloud = WordCloud(width=800, height=600, background_color='white').generate_from_frequencies(wordcloud_data)

plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
