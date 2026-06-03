# 1. Python 装饰器
# 定义
# 装饰器是一种设计模式，用于在不修改函数或类源代码的情况下，动态地增加函数或类的功能。它本质上是一个函数，它接收一个函数作为参数，并返回一个新的函数。
# 作用
# 增强功能：可以在原函数的基础上添加额外的逻辑，比如日志记录、性能测试、权限校验等。
# 代码复用：避免重复编写相同的逻辑代码。
# 解耦：将功能逻辑与附加逻辑分离，使代码更加清晰。
# 基本语法
def decorator(func):
    def wrapper(*args, **kwargs):
        # 在原函数执行前的操作
        print("Before function")
        # 在原函数执行后的操作
        result = func(*args, **kwargs)
        print("After function")
        print(result)
        return result 
    return wrapper

@decorator
def my_function(x):
    print(f"This is my function{x}")

my_function(1)

# 2. Python 迭代器
# 定义
# 迭代器是一个实现了 __iter__() 和 __next__() 方法的对象。它允许我们通过 for 循环或 next() 函数逐个访问容器中的元素，而不需要关心内部的实现细节。
# 特点
# 惰性计算：迭代器不会一次性加载所有数据，而是按需计算下一个值。
# 有限性：迭代器只能向前遍历，不能后退或重新开始，除非重新创建。
class MyIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value
    
#解包：
a, b, *rest = [1, 2, 3, 4, 5]
print(a)      # 输出 1
print(b)      # 输出 2
print(rest)   # 输出 [3, 4, 5]
print(*rest)  # 输出 3 4 5
# 使用迭代器
my_iter = MyIterator(1, 5)
for num in my_iter:
    print(num)

#StopIteration
#在内置迭代器中的使用方式
my_list = [1, 2, 3]
iterator = iter(my_list)
# 列表、字典、集合等容器类型都支持迭代器协议。
# iter() 函数可以将可迭代对象转换为迭代器。
print(next(iterator))  # 输出 1
print(next(iterator))  # 输出 2
print(next(iterator))  # 输出 3
try:
    print(next(iterator))  # 抛出 StopIteration 异常
except StopIteration:
    print('no')


# 3. Python 生成器
# 定义
# 生成器是一种特殊的迭代器，它通过 yield 关键字来生成值。生成器函数在执行到 yield 时会暂停执行，并返回一个值，直到下一次调用 next() 时继续执行。
# 特点
# 惰性计算：生成器按需生成值，不会一次性计算所有结果，节省内存。
# 简化代码：生成器的语法比手动实现迭代器更简洁。


def my_generator(start, end):
    for num in range(start, end):
        yield num

# 使用生成器
gen = my_generator(1, 5)
for num in gen:
    print(num)    ## 类似自动换行输入？
# 生成器表达式
# 类似于列表推导式，但使用圆括号 () 而不是方括号 []：
gen_expr=(x**2 for x in range (5))
for i in gen_expr:
    print(i)
