b=set()
b.add(1)
a={1,2,3,3,2}
print(a)
a.add(6) #加
a.update([7]) 
a.update({23,3})
a.update((100,23))
a.update({10:20})#追加的必须是可迭代对象(列表，元组，集合，字典)
a.remove(3) #减去
a.intersection(b) #返回两个集合的交集
a.union(b) #返回两个集合的并集
a.difference(b) #返回差集
print(a)
print(a&b) # 并集
print(a|b) # 交集
print(a-b) # a有b无
