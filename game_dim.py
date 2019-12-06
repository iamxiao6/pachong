#coding=utf-8
import requests
from requests.exceptions import RequestException
import re
import urllib.request
import pymysql
import time
from datetime import datetime, timedelta

##在各个网站上爬取游戏的名字和类别。需本地安装Mysql

def get_utf8_html(url):
   try:
      response = requests.get(url)  # 拿到网页数据
      response.encoding = 'UFT-8'
      if response.status_code == 200:  # 返回200表示响应正常
         return response.text  # 返回数据
      return None  # 如果响应不正常，则不返回任何数据
   except RequestException as e:  # 所有异常输出为空
      print(e)
      return None

def get_gb_html(url):
   try:
      response = requests.get(url)  # 拿到网页数据
      response.encoding = 'gb2312'
      if response.status_code == 200:  # 返回200表示响应正常
         return response.text  # 返回数据
      return None  # 如果响应不正常，则不返回任何数据
   except RequestException as e:  # 所有异常输出为空
      print(e)
      return None


def get_119_name():##126794
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 119游戏网 start time： %s  ********************' % start_time)

   ##获取119的游戏类别
   web_url = 'https://www.119you.com/search/catagory/1-0-0-0-0.shtml'
   html=get_utf8_html(web_url)
   pattern = re.compile('<dd><a href="/search/catagory/1-0-0(.*?)".*?dataid="(.*?)".*?title="(.*?)"', re.S)
   items = re.findall(pattern, html)  # 以列表形式返回所有能匹配到的字符串
   for type_url,id,type in items:
      url='https://www.119you.com/search/catagory/1-0-0'+str(type_url)##每个类别的url
      type_url = '-0-0' + str(type_url)
      try:
         html = get_utf8_html(url)
         pattern = re.compile('<span>&nbsp;&nbsp;&nbsp;第 1 /(.*?)页', re.S) #获取每个类别的页数
         items = re.findall(pattern, html)[0]
         page=int(items)+1
      except:
         page=9
      print(type, page)
      for i in range(1,page):
         try:
            url='https://www.119you.com/search/catagory/'+str(i)+type_url
            html = get_utf8_html(url)
            pattern = re.compile('class="m-game-item-d">.*?<span class="u-game-name">(.*?)</span>', re.S)
            items = re.findall(pattern, html)  # 以列表形式返回所有能匹配到的字符串
            for name in items:
               try:
                  cursor.execute("insert into game_name (game_name,label) values('%s','%s') "%(name, type))
               except Exception as e:
                  print(e)
                  db.rollback()
                  pass
         except:
            time.sleep(5)
            pass
      db.commit()
   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 119游戏网 end time： %s  ********************' % end_time)
   db.close()


def get_one_name():
   data=[['角色','jiaose'],['快手小游戏','ksxyx'],['第五人格','dwrgyx'],['吃鸡游戏','chiji'],['经典','jingdianyouxi'],['传奇','chuanqisy'],['腾讯','tengxun'],['动作','dzsy'],['体验服','yxtyf'],['仙侠','xianxia'],['即时','jishi'],['国风唯美仙侠','gfwmxxsy'],['养成','yangcheng'],['网易','wangyi'],['策略','celue'],['休闲','xiuxian'],['腾讯吃鸡','txcj'],['3D','3dsy'],['竞技','jingjisy'],['男生','nansheng'],['三国','sanguo'],['丧尸','sangshi']]
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 第一游戏网 start time： %s  ********************' % start_time)
   for type,type_url in data:
      try:
         type_url='http://www.diyiyou.com/zt/'+str(type_url)+'/'
         html = get_utf8_html(type_url)
         print(type)
         pattern = re.compile('> 首页.*?</a>...<a href=.*?">(.*?)</a>', re.S)
         items = re.findall(pattern, html)[0]# 以列表形式返回所有能匹配到的字符串
         page = int(items) + 1
      except:
         page=2

      for i in range(1, page):
         print(type, page)
         try:
            url=type_url+str(i)+'/'
            html = get_utf8_html(url)
            pattern = re.compile('<div class="game_inbox">.*?target="_blank">(.*?)</a>', re.S)
            items = re.findall(pattern, html)  # 以列表形式返回所有能匹配到的字符串
            for name in items:
               try:
                  cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
               except Exception as e:
                  print(e)
                  db.rollback()
                  pass
         except:
            time.sleep(5)
            pass
      db.commit()
   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 第一游戏网 end time： %s  ********************' % end_time)
   db.close()


def get_dyw_name():
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 当游网 start time： %s  ********************' % start_time)
   web_url='http://www.3h3.com/az/d_0_0_55_0_0_1.html'
   html = get_gb_html(web_url)
   pattern = re.compile('<dt><span>分类：</span></dt>(.*?)<dl class="blue">', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile("<a href='/az/d_0_0(.*?)1.html.*?>(.*?)</a>", re.S)
   items = re.findall(pattern, items)
   for url,type in items:
      if type=='全部':
         pass
      else:
         try:
            type_url='http://www.3h3.com/az/d_0_0'+ url+str(1)+'.html'
            html = get_gb_html(type_url)
            pattern = re.compile('<li> <span>共(.*?)页', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1
            print(type,page)
         except:
            page=2
         for i in range(1,page):
            print(type, page)
            try:
               type_url = 'http://www.3h3.com/az/d_0_0' + url + str(i)+'.html'
               html = get_gb_html(type_url)
               pattern = re.compile('<h3 class="tit">.*?target="_blank">(.*?) ', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass
         db.commit()
   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 当游网 end time： %s  ********************' % end_time)
   db.close()


def get_mzw_name():
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 拇指玩 start time： %s  ********************' % start_time)
   web_url='https://www.muzhiwan.com/discovery.html'
   html = get_utf8_html(web_url)
   pattern = re.compile('<li><a href="/discovery/(.*?).html">(.*?)</a', re.S)
   items = re.findall(pattern, html)
   print(items)
   for url,type in items:
      if type=='全部':
         pass
      else:
         try:
            type_url='https://www.muzhiwan.com/discovery/'+ url+'_'+str(1)+'.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('末页</a><span>共(.*?)页', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1
            print(type,page)
         except:
            page=2
         for i in range(1,page):
            try:
               type_url = 'https://www.muzhiwan.com/discovery/' + url + '_' + str(i) + '.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('<a class="i_top".*?title="(.*?)">', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()
   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 拇指玩 end time： %s  ********************' % end_time)
   db.close()

def get_gsy_name():
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 高手游 start time： %s  ********************' % start_time)
   web_url='http://www.gaoshouyou.com/youxiku-0-0-0-0-0-0-1'
   html = get_utf8_html(web_url)
   pattern = re.compile('<dd><a href="//www.gaoshouyou.com/youxiku-0-0(.*?)1".*?>(.*?)</a>', re.S)
   items = re.findall(pattern, html)
   print(items)
   for url,type in items:
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url='http://www.gaoshouyou.com/youxiku-0-0'+ url+str(1)
            html = get_utf8_html(type_url)
            pattern = re.compile('分页快速跳转.*?>...</span><a href="//www.gaoshouyou.com/youxiku-0-0.*?">(.*?)</a><a', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1
            print(type,page)
         except:
            page=2
         for i in range(1,page):
            try:
               type_url = 'http://www.gaoshouyou.com/youxiku-0-0'+ url+str(i)
               html = get_utf8_html(type_url)
               pattern = re.compile('<div class="game-name">.*?target="_blank">(.*?)</a>', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 高手游 end time： %s  ********************' % end_time)
   db.close()

def get_7230_name():
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 7230 start time： %s  ********************' % start_time)
   web_url='http://www.7230.com/tags/'
   html = get_utf8_html(web_url)
   pattern = re.compile('<a href="/tag/(.*?)".*?target="_blank">(.*?)</a>', re.S)
   items = re.findall(pattern, html)
   print(items)
   for url,type in items:
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'http://www.7230.com/tag/' + str(url) + '/' + str(1) + '.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('<a class="end" href="http://www.7230.com/tag/.*?/(.*?).html', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'http://www.7230.com/tag/' + str(url) +'/'+str(i)+'.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('class="title" target="_blank">(.*?)</a>', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 7230 end time： %s  ********************' % end_time)
   db.close()

def get_qd_name():
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 起点软件园 start time： %s  ********************' % start_time)
   web_url='http://www.cncrk.com/shouji/r_18_1.html'
   html = get_utf8_html(web_url)
   pattern = re.compile('<a href="/shouji/s_(.*?)_.*?">(.*?)</a', re.S)
   items = re.findall(pattern, html)
   print(items)

   for url,type in items:
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'http://www.cncrk.com/shouji/s_' + str(url) + '_' + str(1) + '.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('<div class="list_fy">.*?<b>1</b>/(.*?) ', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'http://www.cncrk.com/shouji/s_' + str(url) + '_' + str(i) + '.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('<span class="span_title"><em class="name">(.*?) ', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 起点软件园 end time： %s  ********************' % end_time)
   db.close()


def get_qq_name():##趣趣手游网
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 趣趣手游网 start time： %s  ********************' % start_time)

   for j in range(1,4):
      web_url='http://www.ququyou.com/zt/index_'+str(j)+'.html'
      html = get_utf8_html(web_url)
      pattern = re.compile('<div class="inf"><p class="name"><a href="(.*?)".*?target="_blank">(.*?)</a>', re.S)
      items = re.findall(pattern, html)
      print(items)
      for url,type in items:
         type=type.replace('手游','')
         type = type.replace('游戏', '')

         if type in ('全部','手游下载'):
            pass
         else:
            try:
               type_url = str(url)
               html = get_utf8_html(type_url)
               pattern = re.compile('下一页</a>.*?index_(.*?).html', re.S)
               items = re.findall(pattern, html)[0]
               page = int(items) + 1

            except:
               page=9
            print(type, page)
            for i in range(1,page):
               try:
                  type_url = str(url)+'/index_'+str(i)+'.html'
                  html = get_utf8_html(type_url)
                  pattern = re.compile('<p class="tit">.*?target="_blank">(.*?)</a>', re.S)
                  items = re.findall(pattern, html)
                  for name in items:
                     try:
                        cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                     except Exception as e:
                        print(e)
                        db.rollback()
               except:
                  time.sleep(5)
                  pass

            db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 趣趣手游网 end time： %s  ********************' % end_time)
   db.close()


def get_2265_name(): ##2265
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 2265 start time： %s  ********************' % start_time)
   web_url='http://www.2265.com/game/r_89_1.html'
   html = get_gb_html(web_url)
   pattern = re.compile('<a href="/game/s(.*?)1.html">(.*?)<em', re.S)
   items = re.findall(pattern, html)
   print(items)
   for url,type in items:
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'http://www.2265.com/game/s' + str(url)  + str(1) + '.html'
            html = get_gb_html(type_url)
            pattern = re.compile('页次:<b>1</b>/(.*?) ', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'http://www.2265.com/game/s' + str(url) + str(i) + '.html'
               html = get_gb_html(type_url)
               pattern = re.compile('<dl id="listCont">(.*?)<style>', re.S)
               items = re.findall(pattern, html)[0]
               pattern = re.compile('alt="(.*?)"', re.S)
               items = re.findall(pattern, items)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 2265 end time： %s  ********************' % end_time)
   db.close()

def get_9k9k_name():##9k9k
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 9K9K start time： %s  ********************' % start_time)
   web_url='https://www.9k9k.com/shouyou/youxi/0/0/0/'
   html = get_utf8_html(web_url)
   pattern = re.compile('class="search_keyword" title=".*?" data-id="1_(.*?)">(.*?)</a', re.S)
   items = re.findall(pattern, html)
   print(items)

   for url,type in items:
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'https://www.9k9k.com/shouyou/youxi/' + str(url) + '/0/0/' + str(1)
            html = get_utf8_html(type_url)
            pattern = re.compile('<div class="pagecode">.*?</a>...<a href=".*?">(.*?)</a>', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'https://www.9k9k.com/shouyou/youxi/' + str(url) + '/0/0/' + str(i)
               html = get_utf8_html(type_url)
               pattern = re.compile('<a class="game_name".*?title="(.*?)">', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 9K9K end time： %s  ********************' % end_time)
   db.close()


def get_dwyx_name():##多玩游戏
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 多玩游戏 start time： %s  ********************' % start_time)
   web_url='http://sy.duowan.com/'
   html = get_utf8_html(web_url)
   pattern = re.compile('<h3>按类型查找</h3>(.*?)<li class="item-nav">', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile(' <a data-href href="//sy.duowan.com/list-(.*?)-.*?">(.*?)<i>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'http://sy.duowan.com/list-' + str(url) + '-' + str(1) + '-0.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('<li class="page-disable">.*?title="第(.*?)页', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'http://sy.duowan.com/list-' + str(url) + '-' + str(i) + '-0.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('<a class="item-title".*?title="(.*?)">', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 多玩游戏 end time： %s  ********************' % end_time)
   db.close()

def get_awaz_name(): ##爱吾安卓游戏
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 爱吾安卓游戏 start time： %s  ********************' % start_time)
   web_url='https://www.25game.com/Android/'
   html = get_utf8_html(web_url)
   pattern = re.compile("<li><a href='/Android/(.*?)'>(.*?)</a>", re.S)
   items = re.findall(pattern, html)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'https://www.25game.com/Android/' + str(url) + '0/0/'+str(1)+'/'
            html = get_utf8_html(type_url)
            pattern = re.compile('<span>下一页</span>.*?0/0/(.*?)/', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'https://www.25game.com/Android/' + str(url) + '0/0/' + str(i) + '/'
               html = get_utf8_html(type_url)
               pattern = re.compile('class="left user_icon" title="(.*?) ', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 爱吾安卓游戏 end time： %s  ********************' % end_time)
   db.close()


def get_yx_name(): ##游侠
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 游侠 start time： %s  ********************' % start_time)
   web_url='http://m.ali213.net/game/0-0-0-0-0-1.html'
   html = get_utf8_html(web_url)
   pattern = re.compile('<div class="list_type_con">(.*?)<div class="daily_week">', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile('<a href="(.*?)1.html.*?">(.*?)</a>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'http://m.ali213.net/game/' + str(url) + str(1)+'.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('>下一页</a.*?0-0-0-0-(.*?).html', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=11
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'http://m.ali213.net/game/' + str(url) + str(i) + '.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('.html" target="_blank" title="(.*?)"', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 游侠 end time： %s  ********************' % end_time)
   db.close()



def get_87G_name(): ##87G
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 87G start time： %s  ********************' % start_time)
   web_url='http://www.87g.com/youxi/zhaoyouxi.html'
   html = get_utf8_html(web_url)
   pattern = re.compile('<li style="border:0"><span>游戏类型：</span>(.*?)</li>', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile('<a href="(.*?)1.html">(.*?)</a>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url =  str(url) + str(1)+'.html'
            html = get_utf8_html(type_url)
            pattern = re.compile('>上一页</a> <.*? ..<a href=".*?">(.*?)</a>', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = str(url) + str(i) + '.html'
               html = get_utf8_html(type_url)
               pattern = re.compile('<div class="con">.*?alt="(.*?)"', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 87G end time： %s  ********************' % end_time)
   db.close()

def get_yxwg_name(): ##游戏王国
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 游戏王国 start time： %s  ********************' % start_time)
   web_url='https://www.noyes.cn/games/index_1.html'
   html = get_utf8_html(web_url)
   pattern = re.compile('<dt><a href="//www.noyes.cn/online/">手机网游</a></dt>(.*?)</dd>', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile('<a href="//www.noyes.cn/online/0-(.*?)-.*?">(.*?)</a>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = 'https://www.noyes.cn/games/0-' +str(url)+'-0-'+ str(1)+'/'
            html = get_utf8_html(type_url)
            pattern = re.compile('下一页</a>.*?0-.*?0-(.*?)/', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=9
         print(type, page)
         for i in range(1,page):
            try:
               type_url = 'https://www.noyes.cn/games/0-' + str(url) + '-0-' + str(i) + '/'
               html = get_utf8_html(type_url)
               pattern = re.compile('<span class="s1">(.*?)</span>', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 游戏王国 end time： %s  ********************' % end_time)
   db.close()

def get_qzw_name(): ##前瞻网
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 前瞻网 start time： %s  ********************' % start_time)
   web_url='http://yx.qianzhan.com/game/search'
   html = get_utf8_html(web_url)
   pattern = re.compile('游戏类型：(.*?)快速搜索：', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile('a href="(.*?)".*?>(.*?)</a>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = str(url)
            html = get_utf8_html(type_url)

            pattern = re.compile('</a><a class="gray">.*?</a><a href=.*?">(.*?)</a>', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=7
         print(type,page)
         for i in range(1,page):
            try:
               type_url = str(url)+'&pn='+str(i)
               html = get_utf8_html(type_url)
               pattern = re.compile('<div class="txt">.*?target="_blank">(.*?)</a>', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 前瞻网 end time： %s  ********************' % end_time)
   db.close()

def get_qzw_name(): ##游戏王国
   db = pymysql.connect("localhost", "root", "123456", "data")  ##连接数据库
   cursor = db.cursor()
   start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 前瞻网 start time： %s  ********************' % start_time)
   web_url='http://yx.qianzhan.com/game/search'
   html = get_utf8_html(web_url)
   pattern = re.compile('游戏类型：(.*?)快速搜索：', re.S)
   items = re.findall(pattern, html)[0]
   pattern = re.compile('a href="(.*?)".*?>(.*?)</a>', re.S)
   items = re.findall(pattern, items)

   print(items)

   for url,type in items:
      type = type.replace('\n', '')
      type = type.replace('\t', '')
      type = type.replace('\r', '')
      type = type.replace(' ', '')
      if type in ('全部','手游下载'):
         pass
      else:
         try:
            type_url = str(url)
            html = get_utf8_html(type_url)

            pattern = re.compile('</a><a class="gray">.*?</a><a href=.*?">(.*?)</a>', re.S)
            items = re.findall(pattern, html)[0]
            page = int(items) + 1

         except:
            page=7
         print(type,page)
         for i in range(1,page):
            try:
               type_url = str(url)+'&pn='+str(i)
               html = get_utf8_html(type_url)
               pattern = re.compile('<div class="txt">.*?target="_blank">(.*?)</a>', re.S)
               items = re.findall(pattern, html)
               for name in items:
                  try:
                     cursor.execute("insert into game_name (game_name,label) values('%s','%s') " % (name, type))
                  except Exception as e:
                     print(e)
                     db.rollback()
            except:
               time.sleep(5)
               pass

         db.commit()

   end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print('******************* 前瞻网 end time： %s  ********************' % end_time)
   db.close()


get_119_name()
get_one_name()
get_dyw_name()
get_mzw_name()
get_gsy_name()
get_7230_name()
get_qd_name()
get_qq_name()
get_2265_name()
get_9k9k_name()
get_dwyx_name()
get_awaz_name()
get_yx_name()
get_87G_name()
get_yxwg_name()
get_qzw_name()

