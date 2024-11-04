from bs4 import BeautifulSoup
import pandas as pd
import requests

#爬取对应视频的弹幕
url = 'https://comment.bilibili.com/755624865.xml'  # url链接
html = requests.get(url)  # 用于解析
html.encoding = 'utf8'  # 编码格式为utf8

soup = BeautifulSoup(html.text, 'lxml')  # 使用bs进行xml的解析
results = soup.find_all('d')  # 进行标签《d》的筛选

comments = [comment.text for comment in results]
print(comments)
comments_dict = {'comments': comments}  # 定义一个字典

df = pd.DataFrame(comments_dict)
df.to_csv('bili_danmu2.csv', encoding='utf-8-sig')  # 保存为csv格式的文件