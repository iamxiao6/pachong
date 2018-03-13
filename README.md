# pachong


 url请自行修改
 for b in range(0,60): 请根据需要爬取的豆瓣账号里的电影数和书籍数将60改成相当的数字

【看过的电影】
先分享下Python代码：

#coding=utf-8
import requests
from requests.exceptions import RequestException
import re
import json
import xlwt
import xlrd

def get_one_page(url):
    try:
        response = requests.get(url)#拿到网页数据
        if response.status_code == 200:#返回200表示响应正常
            return response.text#返回数据
        return None#如果响应不正常，则不返回任何数据
    except RequestException as e:#所有异常输出为空
        print(e)
        return None
n=1
def parse_one_page(html):

    pattern = re.compile('<li class="title">.*?<em>(.*?)</em>.*?<li class="intro">(.*?)</li>.*?<span class="rating(\d)-t"></span>.*?<span class="date">(.*?)</span>.*?<span class="comment">(.*?)</span>', re.S)
    items = re.findall(pattern, html)#以列表形式返回所有能匹配到的字符串

    for item in items:
        global n
        sheet.write(n,0,str(item［0］))
        sheet.write(n,1,str(item［2］))
        sheet.write(n,2,str(item［3］))
        sheet.write(n,3,str(item［4］))
        cut=item［1］.split('/')
        i=4
        for j in cut:
            sheet.write(n,i,str(j))
            i=i+1
        n=n+1
        print(n)

def main(start):
    n=start+1
    url = 'https://movie.douban.com/people/7847299/collect?start='+str(start)+'&sort=time&rating=all&filter=all&mode=grid'
    html = get_one_page(url)
    parse_one_page(html)

try:
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('看过的电影',cell_overwrite_ok=True)
    sheet.write(0,0,'电影名')
    sheet.write(0,1,'评分')
    sheet.write(0,2,'看过的时间')
    sheet.write(0,3,'评价')
    for b in range(0,60):
        m=b*15
        try:
            main(m)
            book.save(r'C:\Users\Administrator\Desktop\movie.xls')
        except Exception as e:
            print(e)
            pass
except Exception as e:
    print(e)


代码目前存在几个问题：

1、当标记一部看过的电影而没有评价时，python会长时间卡在此处然后匹配下一部电影的评价。其他无影响。

2、时间，导演，演员，国家，时长等暂未做区分。爬取看过的电影和爬取top250不同的是 看过的电影里面同一个字段有好几项标签 上映时间，国家，导演，演员，语言，时长等等
比如:
    1987-10-04(东京国际电影节) / 1987-10-23(意大利) / 尊龙 / 陈冲 / 彼得·奥图尔 / 英若诚 / 黄自强 / 丹尼斯·邓恩 / 坂本龙一 / 马吉·汉 / 里克·扬 / 邬君梅 / 田川洋行 / 苟杰德 / 理查德·吴 / 皱缇格 / 陈凯歌 / 吴涛 / 卢燕 / 亨利·欧 / 陈述 / 樊光耀 / 鲍皓昕 / 黄文捷 / Ruzhen Shao / Henry Kyi / 张良斌 / Dong Liang / 康斯坦丁·格雷戈里 / Lucia Hwong / 王涛 / 宋怀桂 / 意大利 / 中国大陆 / 英国 / 法国 / 贝纳尔多·贝托鲁奇 / 163分钟 / 219分钟 (电视版) / 末代皇帝 / 剧情 / 传记 / 历史 / 贝纳尔多·贝托鲁奇 Bernardo Bertolucci / 马克·派普罗 Mark Peploe / 英语 / 汉语普通话 / 日语 / 俄语</li>

用正则表达式获取的是整个字段合并在一起,目前没有了解到相关电影导演国家等的分词包，因此这部分暂时只能用split区分,先码着然后再看看有没有更好的办法。用列表查询法若不是完全匹配则为false




【看过的书】
先分享python代码：
#coding=utf-8
import requests
from requests.exceptions import RequestException
import re
import json
import xlwt
import xlrd
import jieba


def get_one_page(url):
    headers = {
    'Host':'book.douban.com',#domain and others header
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive'
    }
    cook={"Cookie":'ll="118282"; bid=1NZLZuzdI24; push_noty_num=0; push_doumail_num=0; __utma=30149280.294266321.1510738321.1520837012.1520845991.44; __utmz=30149280.1520837012.43.9.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.15942; ap=1; gr_user_id=fcc59a96-40ce-43d3-b4be-1ec75baeb5c4; __utma=81379588.2080260853.1510901847.1520836369.1520845991.9; __utmz=81379588.1519875416.6.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/159428266/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1520845989%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F159428266%2F%22%5D; _pk_id.100001.3ac3=5c07186ba0234b1a.1510901847.10.1520845989.1520837043.; _vwo_uuid_v2=F04E65CE142F4495CECB3DDB3D60203D|a142341ca1af0e633044c8b552098d6d; __yadk_uid=Lr1RIjyeNd1lDCQdvgNNMKNnLzhXfpRK; viewed="4820710_1099275_1657455"; __utmc=30149280; __utmc=81379588; ps=y; dbcl2="159428266:/XURry619Eg"; ck=Px_3; _pk_ses.100001.3ac3=*; __utmb=30149280.1.10.1520845991; __utmt_douban=1; __utmb=81379588.1.10.1520845991; __utmt=1; ct=y'}


    try:
        response = requests.get(url,cookies=cook,headers=headers)#拿到网页数据
        if response.status_code == 200:#返回200表示响应正常
            return response.text#返回数据
        return None#如果响应不正常，则不返回任何数据
    except RequestException as e:#所有异常输出为空
        print(e)
        return None

n=1

def parse_one_page(html):

    pattern = re.compile('title="(.*?)onclick.*?<div class="pub">(.*?)</div>.*?<span class="rating(\d)-t"></span>.*?<span class="date">(.*?)读过</span>.*?<p class="comment">(.*?)</p>', re.S)
    items = re.findall(pattern, html)#以列表形式返回所有能匹配到的字符串


    for item in items:
        global n
        sheet.write(n,0,str(item[0]))
        sheet.write(n,1,str(item[1].split("/")[0]))

        sheet.write(n,2,str(item[2]))
        sheet.write(n,3,str(item[3]))
        sheet.write(n,4,str(item[4]))

        n=n+1
        print(n)

def main(start):
    n=start+1
    url = 'https://book.douban.com/people/159428266/collect?start='+str(start)+'&sort=time&rating=all&filter=all&mode=grid'

    html = get_one_page(url)
    parse_one_page(html)

    #     write_to_file(item)

try:
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('看过的书',cell_overwrite_ok=True)
    sheet.write(0,0,'书名')
    sheet.write(0,1,'作者')

    sheet.write(0,2,'评分')
    sheet.write(0,3,'看过的时间')
    sheet.write(0,4,'评价')
    for b in range(0,50):
        m=b*15
        try:
            main(m)
            book.save(r'C:\Users\Administrator\Desktop\emma.xls')
        except Exception as e:
            print(e)
            pass
except Exception as e:
    print(e)
看过的书的代码需要注意的：
1.看过的书需要伪装Header，里面的useragent及cook需要改成自己浏览器的（应该是需要，可以试一下我的）
2.知识储备有限 正则表达式不知道怎么去掉换行符导致写入excel需要 ctrl+H 将空格全部以空替代掉，另外书名需要去掉" （这部分若有知道的大神请赐教）

另外书籍登录过多当天会被禁止登录哦

