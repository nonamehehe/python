import numpy as np
#1、numpy在不同数据类型之间相互转换,astype()
a=np.array([1,2,3])
array([1, 2, 3])
a=a.astype(np.float64)
array([1., 2., 3.])

#argmin()与argmax()求取最小，最大值的索引。
array([1., 2., 3.])
a.argmin() #0
a.argmax() #2

#np.tile的使用，是将数组按纵向与横向复制几遍。
>>> np.tile(a,(2,2))  #纵向与横向变为2倍
array([[1, 2, 3, 1, 2, 3],
       [1, 2, 3, 1, 2, 3]])
>>> np.tile(a,(2,1))  #纵向变为2倍
array([[1, 2, 3],
       [1, 2, 3]])

#np.isnan(),np.isinf(),处理numpy中的nan与inf数据。
a = np.array([[np.nan, np.nan, 1, 2], [np.inf, np.inf, 3, 4], [1, 1, 1, 1], [2, 2, 2, 2]])
where_are_nan = np.isnan(a)
where_are_inf = np.isinf(a)
a[where_are_nan] = 0
a[where_are_inf] = 0




























