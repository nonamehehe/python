# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 06:53:56 2021

@author: Administrator
"""
#————————————————————————————————————————————————————————————————————————总操作集合——————————————————————————————————————————————————————————
#————数据处理001————
#————数据筛选002————

#————数据操作002————


import pandas as pd
import numpy as np
#————————————————————————————————数据处理001————————————————————————————————————
#1、判断数据是否缺失，出现NaN数据。
df.isnull()		#是否为空值。
df.notnull()	#是否不为空值。
#2、对空数据，进行填补。
df.fillna('x')	#用任意数值或字符串X替代NaN空值。
df.fillna(method = 'pad')	#用前一个数据替换空值。
df.fillna(method = 'bfill')	#bfill=behind fill 用后一个数据替换空值。
df.fillna(df.mean())	#用列平均数来填补空数据。
df.fillna( {'a':6 } )	#a列空值使用6来填充。
#3、str.strip()删除数据中字符左右两边的空格。
df['name'].str.strip()		#删除两边空格，中间空格不删除
df['name'].str.rstrip()		#删除右边空格，左边中间空格不删除
df['name'].str.lstrip()		#删除左边空格，右边中间空格不删除

#————————————————————————————————数据筛选002————————————————————————————————————
df[~df['A']>5]  #取反操作，反向
df[df['A'].isin(['学校'])] #列值是否包含某些字符
df[df['A'].str.contains(['学校'])]#列值是否包含字符,与isin区别在于全部与部分

#数据抽取
df['a'].astype(str)		#将列数据转为str（字符型）。
df['a'].str.slice(0,3)		#提取a列的前三个数据。
df.set_index('a')		#将a列作为索引，不采用默认索引。

df.loc()		#location通过索引提取行数据
df.iloc()		#integer location通过索引号提取行数据
df.ix()		#通过索引提取数据（loc(）或  iloc() ）

df.reset_index()		#重置索引，原索引作为新增列
df.reset_index(drop=True)	#重置索引，并将原索引丢弃

df.reindex(hang)		#用列表hang替换索引
df.reindex(columns = lie)		#用列表lie替换列索引
###数据整理
df.sort_index()		#重新排序（默认为升序）

