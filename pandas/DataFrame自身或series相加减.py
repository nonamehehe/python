# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

#1:DataFrame之间的运算 add(),sub(),mul(),div()
df1 = pd.DataFrame(np.random.randint(0, 150, size=(4, 4)),
                index=['张三', '李四', '王五', '小明'],
                columns=['语文', '数学', '英语', 'Python'])
# df2:成绩表二（相对于df1时，多加了一个人）
df2 = pd.DataFrame(np.random.randint(0, 150, size=(5, 4)),
                index=['张三', '李四', '王五', '小明', '小张'],
                columns=['语文', '数学', '英语', 'Python'])
# 两个成绩相加
print(df1 + df2)
'''
       语文     数学     英语  Python
小张    NaN    NaN    NaN     NaN
小明  122.0  154.0  142.0   203.0
张三  108.0   33.0  114.0    64.0
李四  216.0  214.0   66.0   225.0
王五  100.0  214.0   72.0   207.0
'''
# 使用add() 为了避免加起来有NaN的值 fill_value=True
df3 = df1.add(df2, fill_value=0)
print(df3)
'''       语文     数学     英语  Python
小张   62.0  113.0  119.0   112.0
小明  122.0  154.0  142.0   203.0
张三  108.0   33.0  114.0    64.0
李四  216.0  214.0   66.0   225.0
王五  100.0  214.0   72.0   207.0 
'''

#2、Series与DataFrame之间的运算
df3 = pd.DataFrame(np.random.randint(0, 150, size=(5, 4)),
                index=['张三', '李四', '王五', '小明', '小张'],
                columns=['语文', '数学', '英语', 'Python'])
# 提取一列
s1 = df3['Python']  # 提取后是Series类型，是列数据
print(s1)
'''
张三     37
李四     80
王五    139
小明     17
小张     71
Name: Python, dtype: int32
'''
# 然后使用运算符直接相加
print(df3 + s1)
'''
    Python  小张  小明  张三  数学  李四  王五  英语  语文
张三     NaN NaN NaN NaN NaN NaN NaN NaN NaN
李四     NaN NaN NaN NaN NaN NaN NaN NaN NaN
王五     NaN NaN NaN NaN NaN NaN NaN NaN NaN
小明     NaN NaN NaN NaN NaN NaN NaN NaN NaN
小张     NaN NaN NaN NaN NaN NaN NaN NaN NaN
'''
#loc的用法，取出一行的数据
s2 = df3.loc['小明']
print(s2)
'''
语文        105
数学        116
英语         65
Python     17
Name: 小明, dtype: int32
'''
'''
    直接加的，会有类似于广播机制的问题，就是说，
    取出来的这样一行，给df3的每行都会加
'''
print(df3 + s2)
'''
    语文   数学   英语  Python
张三  247  181  170      54
李四  120  175  153      97
王五  182  164  199     156
小明  210  232  130      34
小张  169  133   69      88
'''
'''想要避免NaN值，使用pandas提供的函数'''
df4 = pd.DataFrame(np.random.randint(0, 150, size=(5, 4)),
                index=['张三', '李四', '王五', '小明', '小张'],
                columns=['语文', '数学', '英语', 'Python'])
print(df4)
'''
     语文   数学   英语  Python
张三   27  116   75      87
李四   56  118   82     133
王五   26   60   96      41
小明  140   29  107      20
小张   95  145  119     110
'''
s3 = df4.Python  # 取出列
# axis=0 以列为单位操作，取出的什么就以什么为单位
# 把取出来的数据给df的每列进行相加
print(df4.add(s3, axis=0))
'''
     语文   数学   英语  Python
张三  114  203  162     174
李四  189  251  215     266
王五   67  101  137      82
小明  160   49  127      40
小张  205  255  229     220
'''
s4 = df4.loc['小明']  # 取出行
# axis=1 以行为单位操作，取出的什么就以什么为单位
# 把取出来的数据给df的每行进行相加
print(df4.add(s4, axis=1))
'''
     语文   数学   英语  Python
张三  167  145  182     107
李四  196  147  189     153
王五  166   89  203      61
小明  280   58  214      40
小张  235  174  226     130
'''





















