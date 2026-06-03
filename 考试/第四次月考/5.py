from functools import lru_cache
import array
n,l,m=map(int,input().split())
co1=list(map(int,input().split()))
co2=list(map(int,input().split()))
co3=list(map(int,input().split()))
dp=[0]*m
@lru_cache(maxsize=None)
def f(r,dp):
    if r==1:
        return array.array('h',dp)
    else:
        if r%2==0:
            newdp=array.array('h',dp)
            dp1=f(r//2,dp)
            for i in range(m):
                for j in range(m):
                    newdp[(i+j)%m]+=dp1[i]*dp1[j]
            return newdp
        else:
            newdp=array.array('h',dp)
            dp1=f((r+1)//2,dp)
            dp2=f(r//2,dp)
            for i in range(m):
                for j in range(m):
                    newdp[(i+j)%m]+=dp1[i]*dp2[j]
            return newdp
for i in co1:
    dp[i%m]+=1
if l==2:
        an=[[0]*m for i in range(n)]
        ans=0
        for k in range(n):
            for t in range(m):
                an[k][(t+co2[k])%m]+=dp[t]
        for k in range(n):
            ans+=an[k][(m-co3[k])%m]
        ans=ans%1000000007
        print(ans)
        exit()
dp2=[0]*m
for i in co2:
    dp2[i%m]+=1
dp1=f(l-2,tuple(dp2))
newdp=[0]*m
for i in range(m):
    for j in range(m):
        newdp[(i+j)%m]+=dp1[i]*dp[j]
dp=newdp
an=[[0]*m for i in range(n)]
ans=0
for k in range(n):
    for t in range(m):
        an[k][(t+co2[k])%m]+=dp[t]
for k in range(n):
    ans+=an[k][(m-co3[k])%m]
ans=ans%1000000007
print(ans)


# for j in range(l-1):
#     if j==l-2:
#         an=[[0]*m for i in range(n)]
#         ans=0
#         for k in range(n):
#             for t in range(m):
#                 an[k][(t+co2[k])%m]+=dp[t]
#         for k in range(n):
#             ans+=an[k][(m-co3[k])%m]
#     else:
#         newdp=[0]*m
#         for i in range(n):
#             for t in range(m):
#                 newdp[(t+co2[i])%m]+=dp[t]
#         dp=newdp
# ans=ans%1000000007
# print(ans)
import array

def multiply(a, b, m):
    """数组卷积（模m），复用内存减少开销"""
    res = array.array('i', [0] * m)  # 用int类型避免溢出，内存比short更稳定
    for i in range(m):
        if a[i] == 0:
            continue  # 跳过0，减少无效计算
        for j in range(m):
            if b[j] == 0:
                continue
            res[(i + j) % m] = (res[(i + j) % m] + a[i] * b[j]) % 1000000007  # 提前取模，避免数值过大
    return res

def matrix_pow(arr, power, m):
    """迭代版快速幂（数组形式），无缓存，复用内存"""
    # 初始化结果为"单位元"（相当于矩阵的单位矩阵，卷积后不改变原数组）
    result = array.array('i', [0] * m)
    result[0] = 1  # 只有索引0为1，其他为0
    
    base = array.array('i', arr)  # 复制原始数组作为底数
    while power > 0:
        if power % 2 == 1:
            # 奇数时，结果 = 结果 * 底数
            result = multiply(result, base, m)
        # 底数自乘，power减半
        base = multiply(base, base, m)
        power = power // 2
    return result

# 读取输入
n, l, m = map(int, input().split())
co1 = list(map(int, input().split()))
co2 = list(map(int, input().split()))
co3 = list(map(int, input().split()))

# 初始化dp1（co1的模m计数）
dp = [0] * m
for num in co1:
    dp[num % m] += 1
dp = array.array('i', dp)  # 转为array提升计算效率

if l == 2:
    ans = 0
    # 直接计算，无需创建an数组（节省n*m的内存）
    for k in range(n):
        c2 = co2[k] % m
        c3 = co3[k] % m
        # 目标：t + c2 ≡ -c3 mod m → t ≡ (-c2 -c3) mod m
        target_t = (-c2 - c3) % m
        ans = (ans + dp[target_t]) % 1000000007
    print(ans)
    exit()

# 计算dp2（co2的模m计数）
dp2 = [0] * m
for num in co2:
    dp2[num % m] += 1
dp2 = array.array('i', dp2)

# 快速幂计算 dp2^(l-2)，无缓存
dp_pow = matrix_pow(dp2, l - 2, m)

# 计算 dp = dp1 * dp2^(l-2)（卷积）
newdp = multiply(dp, dp_pow, m)

# 计算最终答案（无需创建an数组，直接累加）
ans = 0
for k in range(n):
    c2 = co2[k] % m
    c3 = co3[k] % m
    # 目标：t + c2 ≡ -c3 mod m → t ≡ (-c2 -c3) mod m
    target_t = (-c2 - c3) % m
    ans = (ans + newdp[target_t]) % 1000000007

print(ans % 1000000007)    
        

   