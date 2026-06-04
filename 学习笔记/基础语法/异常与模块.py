#异常：一个事件，此事在程序执行中发生，影响程序正常执行
#异常处理：
#1
try:
       print(a)
except:  #基类异常
       print('出现错误')

#2
try:
       print(a)
except NameError as e:
       print(e)

#3
try:
       print(a)
except Exception as e:   #万能异常
       print(e)

#4 多分支异常
try:
       print(a)
except IndexError as e:
       print(e)
except KeyError as e:
       print(e)
except NameError as e:
       print(e)       
else:
       print('ok')
finally:
       print('下一步')

try:
       n=int(input('请输入一个整数'))
       print(10/n)
except ValueError:
       print('请输入正确数据')
except Exception as e:
       print('未知错误%s'%e) #如果为ValueError,就不会执行这行
else:
       print('wait a minute')
finally:
       print('go')


#异常传递
#1.
def funa():  #子函数
       return int(input('请输入整数'))
def funb():
       return funa()
try:
       print(funb())
except Exception:
       print('no')

#抛出异常
#1.创建一个Exception('。。。')的对象
#2.raise 抛出 （相当于print）

def user():
    pwd=input('请输入密码：')
    if len(pwd)<6:
           raise Exception('长度不够')
try:
    upwd=user()
    print(upwd)
except Exception as e:   
       print(e)


#使用assert语句抛出异常
#assert 表达式 [,异常信息]
# 说明：
# aseert后面 跟一个表达式，表达式的值为True时不做任何操作，为False时触发AssertionError异常
# 表达式之后可以用字符串来描述异常信息
num_one = int(input("输入被除数:"))
num_two = int(input("输入除数:"))
assert num_two != 0,"除数不能为0"   #assert语句判断除数不等于0
result = num_one/num_two
print(num_one,'/',num_two,'=',result)


#自定义异常
#自定义异常的方法比较简单：只需要定义一个继承 Exception类或Exception子类 的类即可，这个类一般以Error结尾。

class ShortInputError(Exception):
    """自定义异常类"""
    def __init__(self,length,atleast):
        self.length = length            #输入的密码长度
        self.atleast = atleast          #限制的密码长度
 
 
try:
    text = input("输入密码:")
    if len(text) < 3:                       #如果输入密码的长度小于3,那么就抛出ShortInputError异常
        raise ShortInputError(len(text),3)
except ShortInputError as error:
    print("ShortInputError:输入的长度是%d,长度至少是%d" %
          (error.length,error.atleast))
else:
    print("密码设置成功")
 

#模块 
#即.py 文件，查找方便
#内置模块 
import builtins
print(builtins)


#2. 库
#安装 pip.install 模块名

#3.自定义模块

#使用模块
#1.import 导入 2. 模块名.函数/关键字
import 排序  #此处也会输出'排序'中的要输出的东西
print(排序.bubble_sort([1,2,234,1,2]))

#别名
import 排序 as a

#from ... import ...,...
import random
print(random.randint(1,5))

from random import randint
print(randint(1,5))

#py文件的两种功能
#1.脚本：一个文件就是整个文件，直接运行
#__name__='__main__' 表示代码直接在当前文件运行
#2.作为模块导入其他文件执行
#此时 __name__=模块名
print(排序.funa()) #排序



#包
#含有__init__.py文件的文件夹
import 字典
print(type(字典))
import bisect  
#  binary search 二分查找
#  bisect.bisect_left(a,x):find the insertion point i in a list [a].making a[i:] remain sorted(有序) after x is inserted at position i
