1、numpy在不同数据类型之间相互转换
>>> a=np.array([1,2,3])
>>> a
array([1, 2, 3])
>>> a=a.astype(np.float64)
>>> a
array([1., 2., 3.])

2、copy（）函数可以避免改变换数组。
>>> a=np.array([1,2,3])
>>> b=a.copy()[0:2]
>>> b
array([1., 2.])

3、argmin()与argmax()求取最小，最大值的索引。
array([1., 2., 3.])
>>> a.argmin()
0
>>> a.argmax()
2

4、cumsum()函数，累计求和。
>>> b
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
>>> b.cumsum()
array([ 1,  3,  6, 10, 15, 21, 28, 36, 45], dtype=int32)

5、自定义函数，传入array进行数据处理
>>> def f(x):
...     return x+1
...
>>> f(b)
array([[ 2,  3,  4],
       [ 5,  6,  7],
       [ 8,  9, 10]])

6、np.tile的使用，是将数组按纵向与横向复制几遍。
>>> np.tile(a,(2,2))  #纵向与横向变为2倍
array([[1, 2, 3, 1, 2, 3],
       [1, 2, 3, 1, 2, 3]])
>>> np.tile(a,(2,1))  #纵向变为2倍
array([[1, 2, 3],
       [1, 2, 3]])
       
