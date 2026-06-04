# 读取输入的n和k
n, k = map(int, input().split())
k -= 1  # 转换为0索引

# 预处理阶乘数组，fact[i] 表示i!
fact = [1] * n
for i in range(1, n):
    fact[i] = fact[i-1] * i

# 可用数字列表
available_nums = list(range(1, n + 1))
result = []

# 逐个确定每一位数字
for i in range(n):
    # 当前位的剩余排列数（阶乘值）
    current_fact = fact[n - 1 - i]
    # 计算当前位要选的数字在可用列表中的索引
    idx = k // current_fact
    # 将选中的数字加入结果
    result.append(str(available_nums[idx]))
    # 从可用列表中移除该数字
    del available_nums[idx]
    # 更新k为剩余的偏移量
    k = k % current_fact

# 拼接结果并输出
print(''.join(result))