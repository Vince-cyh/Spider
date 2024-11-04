import requests
import jieba
import time
import csv
from pyecharts.charts import WordCloud

# 得到csv这个对象，一遍下面的存储使用
cfile = open('bilibili评论数据.csv', 'w+', encoding='utf8', newline='')
csv_file = csv.writer(cfile)

url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=897843523&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=3b7099ee68919698814b4e305f089d41&wts=1698583404'
resp = requests.get(url).json()
# 声明一个变量进行计数，我只需要获得200条数据就可以了
count = 0
# 数据清洗得到主评论
for i in resp['data']['replies']:
    # 获取评论id和页数，用作自评的请求参数
    rpid = i['rpid']
    rcount = i['rcount']
    # 获得评论内容
    content1 = i['content']['message']
    # 写入csv文件中
    csv_file.writerow([content1])
    print(rpid, content1)
    count += 1
    """ 请求子评论 """
    # 循环页数发送请求
    for j in range(1, rcount):
        print(j)
        # root 参数为主评论id
        # pn 参数为页数
        url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={j}&type=1&oid=48487753&ps=10&root={rpid}&_=1667134065802'
        resp = requests.get(url).json()
        # 这里可能会得到没有子评论的主评论，要进行为空处理
        if resp['data']['replies'] != None:
            # 有数据之后在进行循环获取，不然会报错
            for m in resp['data']['replies']:
                # 获得评论内容
                content2 = m['content']['message']
                # 写入csv文件中
                csv_file.writerow([content2])
                count += 1
                # 当数据大于200条时，我们就退出程序
                if count > 200:
                    exit()
        # 每发送子评论请求，进行休眠2秒钟，不然ip会被禁掉
        time.sleep(2)