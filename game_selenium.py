#coding=utf-8
import time
import requests
from requests.exceptions import RequestException
import re
import json
import xlwt
import xlrd
import io
import sys
import urllib.request
from selenium import webdriver
browser=webdriver.Chrome() ##弹出窗口
# browser = webdriver.PhantomJS() #不弹出窗口
n=0
book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('魔幻',cell_overwrite_ok=True)
for i in range(1,46):
    url="http://www.9game.cn/search/?keyword=RPG&categoryId=3&page="+str(i)+'/'
    browser.get(url)
    time.sleep(5)
    try:
        for i in range(3):#测试三次下拉
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(1)
    except:
        pass

    html=browser.page_source
    pattern = re.compile('img src="http://image.game.uc.cn/.*?alt="(.*?)" />', re.S)
    items = re.findall(pattern, html)#以列表形式返回所有能匹配到的字符串


    for item in items:  
        n=n+1
        print(n,item)
        sheet.write(n,0,str(item))

print('OK')
book.save(r'C:\Users\jiguang\Documents\2、数据\5、爬虫\游戏分类 20180730\九游\RPG.xls')

