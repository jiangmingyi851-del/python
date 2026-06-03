#传递引用
#id(x) x的内存地址
a=10
b=10
print(id(a))
print(id(b))  #  一致，表明b没有重复存放10，只是引用a的地址，没做数据重复存储

#copy
import copy #  导入copy模块
c=[1,2,3,4,5]
c_copy=copy.copy(c)
print(id(c))
print(id(c_copy)) #  不同，由于拷贝到了另一个地方


#不可变对象：针对的是值（数据内容）来说的，（原数据存放处）内容不可变，地址重新分配
i=73
print(id(i))
print(i)
i+=2
print(id(i)) # 内存地址会变化
# 元组为不可变对象，代码更安全
# int str 也是 


#可变对象 存储数据可在现有地址直接修改
#set,list,dict
