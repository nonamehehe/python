#copy()函数可以避免改变换数组。
>>> a=np.array([1,2,3])
>>> b=a.copy()[0:2]
>>> b
array([1., 2.])

#cumsum()函数，累计求和。
>>> b
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
>>> b.cumsum()
array([ 1,  3,  6, 10, 15, 21, 28, 36, 45], dtype=int32)

#自定义函数，传入array进行数据处理
>>> def f(x):
...     return x+1
...
>>> f(b)
array([[ 2,  3,  4],
       [ 5,  6,  7],
       [ 8,  9, 10]])



#7、np.repeat()函数，是将矩阵延横轴或者纵轴复制几遍。
>>> c
array([[1, 2],
       [3, 4]])
>>> np.repeat(c,2,axis=0)
array([[1, 2],
       [1, 2],
       [3, 4],
       [3, 4]])

#8、numpy.extract() 函数根据某个条件从数组中抽取元素，返回满条件的元素。
>>> x = np.arange(9)
>>> condition = np.mod(x,2)  ==  0 #取偶
>>> print (np.extract(condition, x))
[0 2 4 6 8]









       
