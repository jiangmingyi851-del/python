# strl='hello'
# print(type(strl))
#''' """用在变量定义里，可用来定义多行字符串的内容
# hi='''hello
# hi
# python'''
# print(hi)


#字符串内要双引号？
# print("hello \"w\"ord")
#\:转义符号
#字符串运算符 +：连接 
from opcode import hasname


a='hello'
b='world'
print(a+b)
# *：重复输出
print(a*2)
#  in：成员运算符-若字符串中包含给定的字符就返回True
print('h' in a)
# not in同理
#r\R 原样输出后面内容
print('hello\nhello')
print(r'\nhello')

print((a+'sss'+b+'\n')*2)


#格式化输出：按照我们想要的模式进行输出
#1)定义模板
#2）照着模板输变量
#  1.print('模板'%变量名)
#  2. format() 
#  3.f'{表达式}' 格式输出
# %s 字符串形式输出 %d 有符号的十进制整数 %o 八进制整数 %x 十六进制整数 %f 浮点数
age=18.4
__name__='Ridger'
print('my name is %s,age is %d'%(__name__,age))
#f%
print('%f'% age) # 默认保留六位小数
print('%.2f'% age) #  保留两位小数

#format()
print('{},{}'.format(11,23))
print('方法{} {}'.format(a,b))

#带数字编号，可调换顺序，即{1}，{2}
print('{0},{1},{1},{0}'.format(11,23))#一定要从零开始排列

#设置参数
print('用户名：{nam},网址：{url}'.format(nam='Ridger',url='www.com'))

#f'{}
print(f'名字是：{"we"},年龄是：{20}')
def fname(arg):
    pass
__main__='Ridger'
if __name__ == __main__:
    print(1)

# 字符串
#1)字符串的定义：用引号把内容括起来
# 三引号可用来定义多行字符串
hi='''hello
python'''
print(hi)

    