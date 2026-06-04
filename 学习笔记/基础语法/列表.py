# 有序；可存储不同数据类型
a=['hello_World6','qw',1,2]
print(a[1])

#可用for 读取
#len()求列表元素个数
for i in a:
    print(a)
i=0
while i < len(a):
    i+=1
print(i)

#1. increase
#1) +
#2) insert
# a.insert(0,'s')
# print(a)
t=('a','s') #此时作为整体添加
# a.insert(2,t)
# print(a)

#3) append 末尾追加
a.append(t)
print(a)

#4) extend 末尾追加，但元组会拆出来
a.extend(t)
print(a)

#2. modify a single element

#1)
a[1]=-10
print(a)
#2)
a[1:4]=[12,13,14]
print(a)
#3) 对空切片赋值=插入
a[4:4]=[11,11,11]
print(a)

#3.delete  形式：del listname/listname[index]
s=[1,2,3,4]
# del s[1]
# print(s)
# del s[2:5]
# print(s)

#pop
#listname.pop(index) index 不写 默认最后一个
s.pop()
t=s.pop() #此时列表会再次取出最后一个元素并储存到t中
print(s,t)

#remove() delete appointed element
s.remove(2)
print(s)
d=[1,2,1,1,3]
d.remove(1)
print(d) #delete the first one

#clear() delete all the elements
d.clear()
print(d)

#4.search
#in
#not in 
list1=[1,2,'hello']
# name=input('需要查找的名字是') #注意input默认输入类型为str
# if name in list1:
#     print('yes')
# else:
#     print('no')

#count() 统计某元素数目
print(list1.count(1))
if list1.count(100): #若值为0代表false
    print('yes')
else:
    print('no')

#index 查找某一元素位置
print(list1.index(1))

#5.rank
#reverse() #在原列表上修改 倒置排序
list1.reverse()
print(list1)

#sort()排序
e=[2,4,5,23,4,3]
e.sort() #其相当与一个操作，无返回值，print为none
print(e) #默认升序
e.sort(reverse=True)
print(e)

#sorted 内置函数，不对原本列表修改
b=sorted(e)
print(b)

# bisect 维护有序列表函数
# bisect.bisect 找到应有的插入位置
# bisect.insort 插入应有的位置 


#5. 列表推导式
li=[1,2,3,4,5,6,7]
print([i*2 for i in li]) #简便很多

#for
li2=[]
for i in li:
    li2.append(i*2)
print(li2)

# 6.双冒号   在 Python 中，双冒号 :: 是切片语法的一部分，用于指定序列（如列表、字符串、元组等）的切片操作中的步长（step）。完整的切片语法格式为 [start:stop:step]。
# sequence[start:stop:step]
# 创建一个示例列表
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 每两个元素取一个
print(numbers[::2])  # 输出: [0, 2, 4, 6, 8]

# 从索引1开始，每两个元素取一个
print(numbers[1::2])  # 输出: [1, 3, 5, 7, 9]

# 取前6个元素，每两个取一个
print(numbers[:6:2])  # 输出: [0, 2, 4]
# 反转列表
print(numbers[::-1])  # 输出: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 反转字符串
text = "Hello, World!"
print(text[::-1])  # 输出: "!dlroW ,olleH"
