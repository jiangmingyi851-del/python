#1. + :str tuple list
#   *:str tuple list
#   in:str tuple list dict
#   not in:str tuple list dict

#2. len()
#  del 

#  max()  list  tuple 
#  min
#  range()

#enumerate()  （下标、数据）一一列出，通常用for 遍历
list1=['a','b','c']
for i in enumerate(list1):
    print(i)

#推导式
# list 
li=[i for i in range(10)]
print(li)
# tuple
tl=(b for b in range(10))
print(tl) #  返回的是对象的地址
print(tuple(tl))
# dict
dict1={i:i**2 for i in range(1,5)} 
# set
set1={i**2 for i in range(2,5)}