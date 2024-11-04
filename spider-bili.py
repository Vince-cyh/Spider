import requests
from lxml import etree
import time
import random
import csv
import pandas as pd

def get_target(keyword, page,saveName):
    result = pd.DataFrame()

    for i in range(1, page + 1):
        # headers = {
        #   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}'.format(keyword, i)
        html = requests.get(url.format(i), headers=headers)
        bs = etree.HTML(html.text)

        items = bs.xpath('//ul[@class="video-list clearfix"]/li')
        for item in items:
            video_url = item.xpath('.//a[@class="img-anchor"]/@href')[0].replace("//","")                   #每个视频的来源地址
            title = item.xpath('.//a[@class="img-anchor"]/@title')[0]                  #每个视频的标题
            view_num = item.xpath('.//span[@class="tag-item watch-num"]/span')[0].text.strip('\n        ')         #每个视频的播放量
            danmu = item.xpath('.//span[@title="弹幕"]')[0].text         #弹幕
            upload_time  = item.xpath('.//span[@title="上传时间"]/span')[0].text  # 上传日期
            up_author = item.xpath('.//span[@class="tag-item uper"]//a')[0].text.strip('\n        ')          #up主

            df = pd.DataFrame({'title': [title], 'view_num': [view_num], 'danmu': [danmu], 'upload_time': [upload_time], 'up_author': [up_author], 'video_url': [video_url]})
            result = pd.concat([result, df])

        time.sleep(random.random() + 1)
        print('已经完成b站第 {} 页爬取'.format(i))
    saveName = saveName + ".csv"
    result.to_csv(saveName, encoding='utf-8-sig',index=False)  # 保存为csv格式的文件
    return result

if __name__ == "__main__":
    keyword = input("请输入要搜索的关键词：")
    page = int(input("请输入要爬取的页数："))
    saveName = input("请输入要保存的文件名：")
    get_target(keyword, page,saveName)