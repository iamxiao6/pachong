#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.path.append('/home/caiys/txt/py/game_desc_similarity')
sys.setdefaultencoding( "utf-8" )
import pandas as pd
import numpy as np
from gensim import corpora,models,similarities
import codecs
from operator import itemgetter, attrgetter
import jieba
from datetime import datetime, timedelta
import jieba.analyse

def get_all_text():
	print("正在导入数据")
	words=[]	
	text=pd.read_table('game_all.txt',names=['name','desc','words'])
	file_object = text['words']
	for line in file_object:
		line=str(line).split(',')
		tmp=[]
		for i in line :
			tmp.append(str(i))
		words.append(tmp)
	stopwordlist=[]
	file_object = open('test.txt','rU')
	for line in file_object:
		stopwordlist.append(line.rstrip('\n')) 
	return text,words,stopwordlist

def dispose_train_text():
	print("分词中")
	text=pd.read_table('game.txt',names=['name','desc'])
	jieba.analyse.set_stop_words('test.txt')
	words=[]
	y=0
	f = codecs.open('game_all.txt','w','utf-8')
	# for name,line in text:
	for y in range(0,len(text)):
		line=text['desc'][y]
		name=text['name'][y]	
		f.write(str(name)+'\t')
		f.write(str(line)+'\t')
		# try:
		# 	line=line.replace(text['name'][y],'')
		# except:
		# 	pass
		# cut = jieba.cut(line,cut_all=True)
		cut = jieba.analyse.extract_tags(str(line), 10000000)		

		for i in cut:
			if (len(i)>1):
				f.write(str(i)+',')
			else:
				pass
		f.write('\r\n')
		f.flush()

		if y%10000==0:
			print(y)
		else:pass
					
	f.close()
	# game_all=pd.read_table('game_all.txt',names=['name','desc','words'])
	# return game_all

def dispose_test_text(words,stopwordlist,test_name,test_text):
	print("处理需要计算的文本")
	dictionary = corpora.Dictionary(words)
	# test_text=test_text.replace(test_name, "")
	test_cut=jieba.cut(test_text,cut_all=True)
	test_word=[]
	for i in test_cut:
		if (len(i)>1) and (i not in stopwordlist):
			test_word.append(i)
		else:
			pass
	doc_test_vec = dictionary.doc2bow(test_word)
	return doc_test_vec

def get_top_name(text,words,stopwordlist,doc_test_vec,nums):
	print("获取最相似的游戏")
	dictionary = corpora.Dictionary(words)
	# dictionary.filter_extremes(no_below=1, no_above=1.0, keep_n=10000000)
	corpus = [dictionary.doc2bow(doc) for doc in words]
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	# # lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=4)
	# # lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=4)
	
	# # corpus_lsi = lsi[corpus_tfidf]
	# # corpus_lda = lda[corpus_tfidf]
	index = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=len(dictionary.keys()))
	sim = index[tfidf[doc_test_vec]]
	temp = np.argpartition(-sim, nums)
	result_args = temp[:nums]
	top_name = [[text.loc[i]['name'],text.loc[i]['desc'],sim[i]] for i in result_args]
	# top_name = [[text.loc[i]['name'],sim[i]] for i in result_args]
	return top_name

def write_top_name_to_txt(top_name):
	print("写入txt")
	n=1
	f = codecs.open('sim.txt','w','utf-8')
	for i in top_name:
		f.write(str(n)+'\t')
		f.write(str(i[0])+'\t')
		f.write(str(i[1])+'\t')
		f.write(str(i[2])+'\r\n')
		n=n+1
	f.close()

def load_into_table(top_name,test_name):
	print("导入数据库")
	os.system("hadoop fs -put sim.txt sim.txt" )
	os.system("hive -e \"load data inpath 'sim.txt' overwrite into table tmp.game_desc_similarity_cys partition(label='%s')\" " %(test_name))

def execute_hql(sql):
    os.system("hive -e \"SET mapreduce.job.queuename=root.ad;%s\" " % sql)

def count_imei(test_name):
	print("获取各游戏的用户")
	three_days_before = int((datetime.now() - timedelta(days=3)).strftime('%Y%m%d'))
	half_year_before =int((datetime.now() - timedelta(days=180)).strftime('%Y%m%d'))
	sql="""
			insert overwrite table tmp.game_similarity_imei_cys partition(label='%s')
			select a.id,b.imei,b.name,b.package from (select id,name from tmp.game_desc_similarity_cys where label='%s') a 
			join (select imei,name,package from edw.app_list_fact where data_date=%s and install_type in (0) and from_unixtime(int(substr(last_report_time,0,10)),'yyyyMMdd') >= %s)b on a.name=b.name
			group by a.id,b.imei,b.name,b.package;
		"""%(test_name,test_name,three_days_before,half_year_before)
	print(sql)
	execute_hql(sql)

if __name__ == '__main__':		
	# words=dispose_train_text()
	text,words,stopwordlist=get_all_text()
	nums= 10000
	test_name="茅山异闻录"
	test_text="""茅山异闻录官方安卓公测版是一款角色扮演战斗类手游，畅爽对决夺宝激战，超劲爽战斗玩法，邂逅众多英雄跟你一起踏上伏魔征途，丰富的角色系统让你体验最劲爆的热血之战，身临其境闯荡PK，大型神话PK之战，快来征服这个仙魔世界吧。 茅山异闻录官方版游戏特色： 1、自由PK百战对决，实力争霸夺屏劲战，经典热血传奇之战，与众多英雄一起组队冒险； 2、热血对决畅爽争霸，无双对决攻城出击，解锁更多高级装备，战力飙升一招降魔伏妖； 3、四大职业任性转职，通过副本战斗的模式，结伴盟友夺宝战四方，同屏畅聊，约会萌妹子。 系统玩法： 强化系统： 顾名思义，强化系统是直接提升装备属性的系统，通过消耗低级强化石，高级强化石来提升装备的强化等级，强化等级越高装备属性越强力。当然，强化等级越高，强化成功的难度也会越高，并伴随着失败的风险。 升级系统： 升级，通过消耗对应的装备升级石用以提升装备等级，装备等级越高装备属性越强力。升级到40级以后的装备可以铸造哦！ 宝石系统： 宝石，在游戏中，也是提高玩家装备属性的另外一条路径，玩家可以通过消耗宝石，来提升装备的星级，星级越高，消耗也会越大，当然升星是必定成功的。 品质系统： 装备进阶系统，是游戏中用来进行装备升级的系统，升级品质需要晶石，各阶段需要不同的晶石，可以在品质副本打出来或者再熔炉里合成出来"""
	print(test_name)
	doc_test_vec=dispose_test_text(words,stopwordlist,test_name,test_text)
	top_name=get_top_name(text,words,stopwordlist,doc_test_vec,int(nums))
	top_name=sorted(top_name, key=itemgetter(2), reverse=True)
	write_top_name_to_txt(top_name)
	load_into_table(top_name,test_name)
	count_imei(test_name)

