'''1.find'''
a='hello_World6'
print(a.find('hello')) #0 
print(a.find('h'))   #0
print(a.find('l',1,5)) #2 找到的是第一个l
print(a.find('l',3)) #3 从第三个位置开始找
print(a.find('x'))  #-1 找不到返回-1

'''2.index
与find 唯一区别：找不到字串不会报错'''

'''3.count
查找出现次数'''
print(a.count('l'))
print(a.count('l',3)) #2


#二.修改
#1.replace
mystr='hello_world_'
print(mystr.replace('l','a'))
print(mystr.replace('l','a',2)) #只替换两次

#2.split 分割
print(a.split('_')) #由此分割，变成列表
print(a.split('e'))

#3.capitalize 将第一个字母变大写
print(a.capitalize())

#4.lower 把字符串所有大写变小写
print(a.lower())

#5.upper把小写变大写
print(a.upper())

#6.title 把字符串的每个单词首字母大写
print(a.title())

'''三、判断'''
#1.islower 检测是否全小写
print(a.islower())

#2.isupper

#3.isdidit()是否为数字
j=0
for i in a:
    if i.isdigit(): #判断字符串里每个字符是否为数字
        j+=1
print(j)   


#4.startswith
print(a.startswith('h'))

#5.endwith

'''四、增'''
#1.加
name='yes'
info=name+a
print(info)
 
#join
b='hello'
#???不能用。

#rstrip delet right space
#strip  delet both space
c='\n\titcast\t\n'
print(c)
print(c.strip()) 