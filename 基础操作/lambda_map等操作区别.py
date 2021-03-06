﻿一、元素-表达式：
lambda argument_list：expression
1、lambda x, y: x*y     函数输入是x和y，输出是它们的积x*y
add=lambda x, y: x+y
add(1,2)  #add(1,2)=3

二、将lambda函数作为参数传递给其他函数

找出3的倍数：
1、filter（）函数：接收两个参数，一个是函数，一个是序列。将序列中的元素依次传入函数，计算后为返回为True的序列。
list(filter(lambda x: x % 3 == 0, [1, 2, 3]))
输出=[3]

2、map函数：接收两个参数，一个是函数，一个是序列。将序列中的元素依次传入函数，计算后为返回新的序列。
>>> list(map(lambda x: x+1, [1, 2,3]))
[2, 3, 4]

3、reduce函数：需要先入到模块from functools import reduce
接收两个参数，一个是函数，一个是序列
In [181]:  reduce(add,(range(5)))
Out[181]:  10


三、i for i in xx if xx 表达式： 
带有i的expression for i in 某范围 if 带i的expression。

可以看成：
 for i in xx：
    if xx：
        doing

例如：
>>> [i+1 for i in range(5) if i>1]
[3, 4, 5]
