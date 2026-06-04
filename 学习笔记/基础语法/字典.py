
# name={}
# name=dict() #空
# dictname[key]=Value 或{'associate key1':value,'associate key2':value......} 添加字典词
# if key in dict 
#del dictname[key]
#dictname.ckear()
#len()
#dictname.keys() return all keys to make a list
#dictname.values() return all values ......
#dictname.items()
e={'a':'w','s':'d'}
print(e.items())
e['er']={'ss':'ser','sr':'srr'}
print(e)
#循环和遍历
#for ......in
for q in e.values():
    print(q)

for s in e: #相当于遍历key
    print(s)

for key,value in e.items():
    print(f'{key}={value}')

Chinese={'小明':85,'小红':72,'小亮':83}
Math={'小明':96,'小红':80,'小亮':69}
English={'小明':88,'小红':91,'小亮':75}
a=0
b=0
c=0
for n in Chinese:
    if n=='小明':
        a+=Chinese[n]
    if n=='小红':
        b+=Chinese[n]
    if n=='小亮':
        c+=Chinese[n]
    print(f'{n}的语文分数是：{Chinese[n]}')
for n in Chinese:
    if n=='小明':
        a+=Math[n]
    if n=='小红':
        b+=Math[n]
    if n=='小亮':
        c+=Math[n]
    print(f'{n}的数学分数是：{Math[n]}')
for n in Chinese:
    if n=='小明':
        a+=English[n]
    if n=='小红':
        b+=English[n]
    if n=='小亮':
        c+=English[n]
    print(f'{n}的英语分数是：{English[n]}')
print(f'小明的总分是：{a}')
print(f'小红的总分是：{b}')
print(f'小亮的总分是：{c}')
rank=[a,b,c]
for i in range(len(rank)-1):
    for j in range(i,len(rank)):
        if rank[i]<rank[j]:
            rank[i],rank[j]=rank[j],rank[i]
    
print(f'总分排名：{rank}')


# Python 字典高效用法笔记（代码示例版）
# 本文档通过代码示例展示字典的低效用法及优化技巧，附带详细注释说明

# 1. 避免将字典仅视为"键值容器"：使用get()方法简化取值逻辑
# 低效写法：通过if-else判断键是否存在
def bad_key_check(my_dict, key):
    if key in my_dict:
        value = my_dict[key]
    else:
        value = 'default'  # 键不存在时返回默认值
    return value

# 高效写法：使用get()方法一步完成取值+默认值设置
def good_key_check(my_dict, key):
    # get()第一个参数为目标键，第二个参数为键不存在时的默认值
    return my_dict.get(key, 'default')


# 2. 避免重复查找：同一键只查询一次
def duplicate_lookup_demo():
    person_info = {'name': 'John', 'age': '29', 'city': 'New York'}
    
    # 低效写法：对'name'键进行两次查找（判断存在+获取值）
    if 'name' in person_info:
        print(f"Name: {person_info['name']}")  # 第二次查找
    
    # 高效写法：用get()存储查询结果，避免重复查找
    email = person_info.get('email')  # 只查询一次
    if email is not None:
        print(f"Email: {email}")


# 3. 使用defaultdict简化计数/分组逻辑
from collections import defaultdict

def count_with_defaultdict(items):
    # 低效写法：手动判断键是否存在
    counts_bad = {}
    for item in items:
        if item in counts_bad:
            counts_bad[item] += 1
        else:
            counts_bad[item] = 1  # 首次出现时初始化
    
    # 高效写法：使用defaultdict自动初始化
    counts_good = defaultdict(int)  # 指定默认值类型为int（默认0）
    for item in items:
        counts_good[item] += 1  # 无需判断，直接累加
    return counts_bad, counts_good


# 4. 善用字典推导式简化字典创建
def dict_comprehension_demo():
    # 传统写法：通过for循环逐个添加键值对
    squares_bad = {}
    for x in range(10):
        squares_bad[x] = x * x
    
    # 高效写法：用字典推导式一行完成
    squares_good = {x: x * x for x in range(10)}  # 格式：{键表达式: 值表达式 for 变量 in 可迭代对象}
    return squares_bad, squares_good


# 5. 避免在迭代时修改字典（防止RuntimeError）
def safe_modify_dict(my_dict):
    # 危险写法：遍历字典时直接删除元素
    try:
        for k, v in my_dict.items():
            if v == 0:
                del my_dict[k]  # 会触发RuntimeError
    except RuntimeError as e:
        print(f"错误示例：{e}")
    
    # 安全写法：遍历字典的键列表（副本）进行修改
    for k in list(my_dict):  # list(my_dict)会创建键的副本
        if my_dict[k] == 0:
            del my_dict[k]  # 操作安全
    return my_dict


# 6. 合理使用setdefault()进行分组操作
def group_with_setdefault(data):
    # 低效写法：手动初始化列表
    groups_bad = {}
    for item in data:
        key = item['category']
        if key not in groups_bad:
            groups_bad[key] = []  # 首次出现时初始化列表
        groups_bad[key].append(item)
    
    # 高效写法：用setdefault()自动初始化
    groups_good = {}
    for item in data:
        # setdefault()：键存在则返回对应值，不存在则设置默认值并返回
        groups_good.setdefault(item['category'], []).append(item)
    return groups_bad, groups_good


# 7. 注意Python 3.7+字典的有序性
def ordered_dict_demo():
    # Python 3.7+ 字典会保留插入顺序（官方规范）
    user = {
        'name': 'Alice',
        'age': 30,
        'city': 'Wonderland',
        'hobbies': ['reading', 'adventuring'],
    }
    
    print("字典的插入顺序：")
    for key, value in user.items():
        print(f"{key}: {value}")  # 输出顺序与定义顺序一致
    
    # 提示：若需严格保证顺序操作（如移动元素位置），建议使用collections.OrderedDict


# 8. 用dict.items()提升迭代效率
def efficient_iteration(my_dict):
    # 低效写法：遍历键时重复查询值
    for key in my_dict:
        print(f"低效迭代：{key} -> {my_dict[key]}")  # 每次都要查询值
    
    # 高效写法：用items()同时获取键和值
    for key, value in my_dict.items():  # items()返回键值对元组的视图
        print(f"高效迭代：{key} -> {value}")  # 无需重复查询


# 演示代码（可直接运行）
if __name__ == "__main__":
    # 1. get()方法演示
    demo_dict = {'a': 1, 'b': 2}
    print("1. get()方法演示：")
    print(f"低效写法结果：{bad_key_check(demo_dict, 'c')}")
    print(f"高效写法结果：{good_key_check(demo_dict, 'c')}\n")
    
    # 2. 避免重复查找演示
    print("2. 避免重复查找演示：")
    duplicate_lookup_demo()
    print()
    
    # 3. defaultdict演示
    print("3. defaultdict演示：")
    items = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    bad_counts, good_counts = count_with_defaultdict(items)
    print(f"计数结果（两种方法一致）：{dict(good_counts)}\n")
    
    # 4. 字典推导式演示
    print("4. 字典推导式演示：")
    bad_squares, good_squares = dict_comprehension_demo()
    print(f"平方字典：{good_squares}\n")
    
    # 5. 安全修改字典演示
    print("5. 安全修改字典演示：")
    test_dict = {'a': 0, 'b': 1, 'c': 0, 'd': 2}
    modified_dict = safe_modify_dict(test_dict)
    print(f"修改后字典（移除值为0的键）：{modified_dict}\n")
    
    # 6. setdefault()演示
    print("6. setdefault()演示：")
    data = [
        {'category': 'fruit', 'name': 'apple'},
        {'category': 'vegetable', 'name': 'carrot'},
        {'category': 'fruit', 'name': 'banana'}
    ]
    bad_groups, good_groups = group_with_setdefault(data)
    print(f"分组结果：{good_groups}\n")
    
    # 7. 有序字典演示
    print("7. 有序字典演示：")
    ordered_dict_demo()
    print()
    
    # 8. 高效迭代演示
    print("8. 高效迭代演示：")
    efficient_iteration({'x': 10, 'y': 20, 'z': 30})

    # 以上示例涵盖了字典的常见低效用法及优化技巧，帮助提升代码性能和可读性。
# 读者可根据实际需求灵活应用
# 拼接方法：'间隔符'.join(列表)
words=['I','love','Python']
sentence=' '.join(words)
print(sentence)
