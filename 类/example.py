# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 11:40:59 2020

@author: Administrator
"""
#——————001类变量————————
class Student:
    name = 'lvl'  #类变量
    age = 32   #类变量
    
stu = Student()   #类实例化
print(stu.name)   #实例对象调用类变量
print(stu.age)  #同上
print(Student.name)  #类对象 调用类变量



#创建一个简单的类，如同构建工厂一般。
class BuildRobot():
    def __init__(self,armcount,headcount):
        self.armcount = armcount
        self.headcount = headcount
    def paintarm(self,color):
        print("paint arm:",color)
#传入参数，如同开始生产订单  
normal_robot = BuildRobot(2,1)  
normal_robot.armcount  # Out[*]: 2
#先class创建instance（实例），才能调用method（方法）
colorful_robot = BuildRobot(2,1)#创建实例
colorful_robot.paintarm('red') #调用方法

# self决定能否调用
class BuildRobot():
    def __init__(self,armcount,headcount):
        armcount = armcount
        headcount = headcount
    def paintarm(self):
        print(armcount)
        
normal_robot = BuildRobot(2,1)
normal_robot.armcount  # Out[*]: AttributeError: 'BuildRobot' object has no attribute 'armcount'
normal_robot.paintarm() # Out[*]: NameError: name 'armcount' is not defined

class BuildRobot():
    def __init__(self,armcount,headcount):
        self.armcount = armcount
        self.headcount = headcount
    def paintarm(color):
        print("paint arm:",color)
        
colorful_robot = BuildRobot(2,1)#创建实例
colorful_robot.paintarm('red') # Out[*]: TypeError: paintarm() takes 1 positional argument but 2 were given

#实例属性与类属性
class Circle(object):
   pi = 3.14  # 类属性
   def __init__(self, r):
       self.r = r

circle1 = Circle(1)
circle2 = Circle(2)

print('----未修改前-----')
print('pi=\t', Circle.pi)
print('circle1.pi=\t', circle1.pi)  #  3.14
print('circle2.pi=\t', circle2.pi)  #  3.14
print('----通过类名修改后-----')
Circle.pi = 3.14159  # 通过类名修改类属性，所有实例的类属性被改变
print('pi=\t', Circle.pi)   #  3.14159
print('circle1.pi=\t', circle1.pi)   #  3.14159
print('circle2.pi=\t', circle2.pi)   #  3.14159
print('----通过circle1实例名修改后-----')
circle1.pi=3.14111   # 实际上这里是给circle1创建了一个与类属性同名的实例属性
print('pi=\t', Circle.pi)     #  3.14159
print('circle1.pi=\t', circle1.pi)  # 实例属性的访问优先级比类属性高，所以是3.14111   
print('circle2.pi=\t', circle2.pi)  #  3.14159
print('----删除circle1实例属性pi-----')
del circle1.pi
print('pi=\t', Circle.pi)
print('circle1.pi=\t', circle1.pi)
print('circle2.pi=\t', circle2.pi)




