

row=['a','s','d']
print(''.join(f"{num:4}" for num in row))
# 1.fstring
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age} years old.")
# 输出: My name is Alice and I'm 25 years old.

# 格式化数字
num = 3.14159
print(f"Pi: {num:.2f}")  # 保留两位小数
# 输出: Pi: 3.14

# 宽度和对齐
print(f"{num:10}")      # 宽度10，右对齐(默认)
print(f"{num:<10}")     # 宽度10，左对齐
print(f"{num:^10}")     # 宽度10，居中对齐
print(f"{num:*>10}")    # 宽度10，右对齐，用*填充

#格式化字符串字面值x = 10
x=10
print(f"{x=}")  # 输出: x=10
