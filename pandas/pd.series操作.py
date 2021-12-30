# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 11:56:19 2021

@author: EDZ
"""
import numpy as np
import pandas as pd
#1、equals()函数：判断两个Series是否相同。
df1 = pd.DataFrame(np.random.randint(10,size=(3,4)))
df2 = pd.DataFrame(np.random.randint(10,size=(3,4)))
df1.equals(df2)

#2、Series转dataframe, T转置, 取max生成新列
Series0 = pd.DataFrame(np.random.randint(10,size=(5,1)))[0]
Series1 = pd.DataFrame(np.random.randint(10,size=(5,1)))[0]
pd.DataFrame([Series0,Series1]).T.max(axis=1) #生成两列最大值 新列
