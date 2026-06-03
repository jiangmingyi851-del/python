#  函数
def fname(arg):
    pass

#函数说明文档查看
#1.help（）
# import random
# help(random) #查看模块
# help(print)

#2.__doc__
print(print.__doc__)

def sing():
    print('唱歌')
#此时不会调用
sing()

#函数：封装有独立的功能，可以调用，函数名()
#方法：在类中的说法，通过 对象来进行，对象.方法
#关键字
help('keywords')

#return 返回给调用处
def funa():
    a=19
    return a 
print(funa())

def hi():
    return 1,2,3 #以tuple形式返回
print(hi())

#一个函数多个return,输出第一个return(只有第一个有效，此时函数结束)

#若无return
def show(x):
    print(x)
show(6)
print(show(6)) #=return none

#参数
def add(a,b):
    return a+b
print(add(10,2))

#默认参数 
#有传参————更新，无则默认
def f(a=12):
    print(f'a={a}')
f()

#不定长参数 *args  *后也可以是其他名字
#接受多个值，以元组形式接受
def  h(*args):
    print(args,type(args))
h(1,2,3)

#关键字参数 **kwargs   传参形式： key=value
def funa(**kwargs):
    print(kwargs)
funa(name='waaks',d='s') # 以字典形式返回

#命名关键字：若前有不定参数，默认后为命名关键字/关键字参数；
# 若前面无不定长参数，加*则将默认后面参数变为命名关键字/关键字参数，需按此传参
def h(a,s,*,c='hook',j):
    print(a,s,c,j)
h('dee','2',c='h',j='d')
h('s',12,j='d')

#混合参数 传参默认顺序：必选、默认、可变、命名关键字/关键字参数
def g(a,c=10,*b,d=55):
    print(f'a={a}')
    print(f'b={b}')
    print(f'c={c}')
    print(f'd={d}')
g(1,2,3,4,5,6,7)


#嵌套 
def funa():
    def funb():
        print('a')
    print('b')
    funb()
funa()

#定义几行的函数
def f():
    print('-'*50)
def g(a):
    for i in range(a):
        f()
g(5)

#random.randint()
import random
c=random.randint(1,6)
print(c)



#作用域：作用的范围
#全局作用域/局部作用域

a=10 # python 会申请空间存放10，将a与10绑定放在名称空间中
#如何清除 del(10)

# 名称空间：内置名称空间：随python执行而产生，停止而结束
# 全局名称空间：执行结束回收
# 局部名称空间：随函数调用而产生，结束而回收，如函数参数，函数内定义的名字
# 不同名称空间不重合，可重名

#作用域与名称空间相似
a=100
def s():
    global a #声明其为全局变量
    a=200 # 修改全局变量
    print(a)
def s1():
    print(a)
s()
s1()
# 可变对象变量 不用声明也行（因为其修改后地址不变）

#nonlocal
#不能修改全局变量
a=10
def funa():
    a=1
    def funb():
        nonlocal a #用的a为外层局部变量,而非全局变量
        print('funb',a)
        a=2
    funb()
    print('funa',a)
funa()
print(a)
#匿名函数
#函数名=lambda 形参：返回值
#lambda 为关键字
def func(a,b):
    return a+b
print(func(1,2))

func=lambda a,b:a+b
print(func(1,2))

#索引字符串某号位
#1
str1='asdfg'
s=[]
s.append(str1[0])
print(s)

#2
func=lambda x:[x[0],x[2]]
print(func('asdfg'))

#三目运算
#1
a=3
b=4
print(a) if a>b else print(b)
#2
func=lambda x,y:x if x>y else y
print(func(3,4))

#内置函数
# import builtins
# print(dir(builtins))

#abs() 返回绝对值
print(abs(-3))

#sum()

#zip() 将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的内容
a=[1,2,3]
b=['a','b','c','d']
print(list(zip(a,b))) # [(1,'a'),(2,'b'),(3,'c')]

# map 
# 对可迭代对象的每一个元素映射，分别执行function
li=[1,2,3,4]
def funa(x):
    return x**2
mp=map(funa,li)
print(list(mp))

print(list(map(lambda x:x**2,li)))

#reduce() 使可迭代对象中元素通过计算不断减少，最终得到一个计算值
#1
from functools import reduce
def func(x,y):
    return x+y
print(reduce(func,[1,2,3,4]))

#2
import functools
l=functools.reduce(func,[1,2,3,4,5])

#enumerate枚举 同时列出下标及数据
for i,j in enumerate([1,2,3,4]):
    print(i,j)


#拆包
def test():
    a=10
    b=20
    c=30
    return a,b,c #以 tuple返回调用处
print(test())
a1,b1,c1=test() #拆包
print(a1)

#用可变参数拆包
tu=(1,2,3,4)
a,*b,c=tu
print(b) #以列表形式输出

#列表拆包

#字典拆包（只输出key,无value)

# 递推函数
# def 函数名([形参表]):
#     if 边界条件:
#         return 结果
#     else:
#         return 递归公式（相当于此处再写一个函数）
def func(num):
    if num == 1:
        return 1
    else:
        return num * func(num - 1)
 
num = int(input("输入一个整数:"))
result = func(num)
print(f"{num}!=%d" % result)
print(f'{num}!={result}')
import numpy

import math

print(math.pi)  # 输出：3.141592653589793
print(math.sqrt(16))  # 输出：4.0
print(math.sin(math.pi / 2))  # 输出：1.0

import random

print(random.randint(1, 10))  # 输出：1到10之间的随机整数
print(random.random())  # 输出：0到1之间的随机浮点数

from datetime import datetime

now = datetime.now()
print(now)  # 输出：当前日期和时间
print(now.year)  # 输出：当前年份
print(now.month)  # 输出：当前月份
print(now.day)  # 输出：当前日期

# 自定义模块可以包含函数、类和变量等。可以通过以下步骤开发自定义模块：
# 创建模块文件：将代码保存到一个.py文件中。
# 组织代码：将相关的函数和类放在模块中。
# 使用__init__.py文件：如果模块是一个包，需要在包目录下创建一个__init__.py文件（可以为空）。
# 导入和使用：使用import语句导入模块，然后调用其中的函数或类。