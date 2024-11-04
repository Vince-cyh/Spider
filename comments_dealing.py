import requests
import jieba
import time
import csv
from pyecharts.charts import WordCloud

# 得到csv这个对象，一遍下面的存储使用
cfile = open('bilibili评论数据.csv', 'w+', encoding='utf8')
csv_file = csv.writer(cfile)

url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=897843523&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=56907605fe4655640b63d1d166a7ab9f&wts=1698582946'
resp = requests.get(url).json()
# 声明一个变量进行计数，我只需要获得200条数据就可以了
count = 0
# 数据清洗得到主评论
for i in resp['data']['replies']:
    # 获取评论id和页数，用作自评的请求参数
    rpid = i['rpid']
    rcount = i['rcount']
    # 获得评论内容
    content = i['content']['message']
    csv_file.writerow([content])
    print(rpid, content)