'''ASC11 编码
GBK 中文编码 双字节
unicode 兼容万国语言
UTF-8:不同字符不定长（中文三字节）英文一字节
encode编码：将字符串换成字节流（二进制数据流）'''
a=b'hello' #字节码 即字节流
print(type(a))
print(a)
b='me'
a1=b.encode()
print(a1)

#解码：将字节流解析（还原为字符串）
a2=a1.decode()
print(a2)

#下标索引：从0开始
name='class_name_sister'
print(name[5])
print(name[6])
#也可倒序索引 从-1始
name2='qwertyuiopadfghjklzxvcbnm'
print(name2[-1])
print(name+name2)


# 切片 [起始索引：结束索引：步长（默认为1）]（左闭右开）
print(name[6:10:1])
print(name[6:10:2])
print(name[:])
print(name[-1:3:-1])
'''倒叙输出'''
#切片可超出范围