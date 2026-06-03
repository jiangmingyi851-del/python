# int(x[,base])  将x转换为一个整数
# float(x)
# complex(real[,imag])
# str(x)
# repr(x) 表达式字符串
# eval(str)
# dict(d) d=(key,value)
# tuple(s)
# list(s)
# chr(x)
# ord(x)
# hex(x)
# oct(x)
# bin(x)
#数据结构类型： str list dict tuple
#'.join(...) 是 Python 中字符串的一个方法，作用是将一个可迭代对象（这里是字符列表）中的元素拼接成一个新字符串。
#其中，'' 表示拼接时使用的分隔符为空字符串（即元素之间无间隔）；join 后的括号内是要拼接的对象（例子中是 ['a', 'e', 't']）。
#
a=123
print(type(a))
a=str(a)
print(type(a))  # 转换

d={'a':1,'b':2,'c':3}
print(set(d)) #只会打印key的内容

#dict()
s=['a1','a2','a3','a4']
c=['b1','b2','b3']
d=zip(s,c)
print(d) #return address
print(dict(d))
