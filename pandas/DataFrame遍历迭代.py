# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 11:38:12 2020

@author: Administrator
"""
#——————————————————————————1、for row in df.iterrows() 将DataFrame行作为（索引，系列）对进行迭代——————————————————————————————
df = pd.DataFrame(np.random.randint(0, 150, size=(4, 4)),
                index=['张三', '李四', '王五', '小明'],
                columns=['语文', '数学', '英语', 'Python'])
print(df)
'''
    语文   数学   英语  Python
张三  55  114  140     123
李四  37  125    3     119
王五  13  136    9      89
小明   1  101   29     118
'''

for row in df.iterrows():
    print(row)
#获的每行的元组格式
''' 
('张三', 语文         55
数学        114
英语        140
Python    123
Name: 张三, dtype: int32)
('李四', 语文         37
数学        125
英语          3
Python    119
Name: 李四, dtype: int32)
('王五', 语文         13
数学        136
英语          9
Python     89
Name: 王五, dtype: int32)
('小明', 语文          1
数学        101
英语         29
Python    118
Name: 小明, dtype: int32)
'''
#row[0]为index，row[1]行内容Series值
for row in df.iterrows():
    print(row[1]['语文'])
   # break
'''
55
37
13
1
'''
for row in df.iterrows():
    print(row[0])
'''
张三
李四
王五
小明
'''  
#——————————————————————————2、for row in df.itertuples()将DataFrame行迭代为namedtuple——————————————————————————————

for row in df.itertuples():
    print(row)
'''
Pandas(Index='张三', 语文=55, 数学=114, 英语=140, Python=123)
Pandas(Index='李四', 语文=37, 数学=125, 英语=3, Python=119)
Pandas(Index='王五', 语文=13, 数学=136, 英语=9, Python=89)
Pandas(Index='小明', 语文=1, 数学=101, 英语=29, Python=118)
'''
for row in df.itertuples():
    print(row[2])
'''
114
125
136
101
'''
#——————————————————————————3、for row in df.items()遍历DataFrame列，返回一个带有列名称和内容为Series的元组——————————————————————————————

for row in df.items():
    print(row)
'''
('语文', 张三    55
李四    37
王五    13
小明     1
Name: 语文, dtype: int32)
('数学', 张三    114
李四    125
王五    136
小明    101
Name: 数学, dtype: int32)
('英语', 张三    140
李四      3
王五      9
小明     29
Name: 英语, dtype: int32)
('Python', 张三    123
李四    119
王五     89
小明    118
Name: Python, dtype: int32)
'''




