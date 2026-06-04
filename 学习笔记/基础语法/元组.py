#元组：不能被修改，不支持删除
num_list=(1,2,3)
print(num_list[0])
# num_list[1]=12  报错
# print(num_list)

#定义单个元素要加‘，’
t2=(10)
print(type(t2))
t2=(10,)
print(type(t2))


#index 
print(num_list.index(1))

#count
#tuple.count(obj)

#4.len

#5.元组可变的情况
t2=(1,2,3,[12,23,34],34,4)
print(t2[3])
# 取到23？
print(t2[3][1])

t2[3][0]=6
print(t2[3])