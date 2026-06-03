num=input()
n=len(num)
target=int(input())
count=0
def mind_pix_to_back_pix(s):
    dic={'+':1,'-':-1,'*':2}
    li=[]
    stack=[]
    for i in s:
        if i.isdigit():
            li.append(int(i))
        else:
            while stack and dic[stack[-1]]>=dic[i]:
                li.append(stack.pop())
            stack.append(i)
    while stack:
        li.append(stack.pop())
    return li
def run_back_pix(li):
    stack=[]
    for i in li:
        if isinstance(i,int):
            stack.append(i)
        else:
            b=stack.pop()
            a=stack.pop()
            if i=='+':
                stack.append(a+b)
            elif i=='-':
                stack.append(a-b)
            else:
                stack.append(a*b)
    return stack[0]


for i in range(1<<(n-1)):
    run=[]
    a=i
    for j in range(n-1):
        run.append(a%2)
        a//=2
    b=sum(run)
    for k in range(3**b):
        s=''
        cu=''
        a=k
        for j in range(n):
            if j==n-1:
                cu+=str(num[j])
                s+=cu
                break
            if run[j]==0:
                cu+=str(num[j])
            else:
                cu+=str(num[j])
                s+=cu
                c=a%3
                if c==0:
                    s+='+'
                elif c==1:
                    s+='-'
                else:
                    s+='*'
                cu=''
                a//=3
        val=eval(s)
        if val==target:
            count+=1
print(count)

# import sys

# def solve():
#     # 读取输入
#     try:
#         input_data = sys.stdin.read().split()
#         if not input_data:
#             return
#         num_str = input_data[0]
#         target = int(input_data[1])
#     except Exception:
#         return

#     n = len(num_str)
#     # 预先将字符串转为数字列表，避免后续反复取下标转换
#     digits = [int(c) for c in num_str]
#     ans = 0

#     def dfs(index, current_val, prev_val):
#         nonlocal ans
        
#         # 终止条件：遍历完所有数字
#         if index == n:
#             if current_val == target:
#                 ans += 1
#             return

#         val = 0
#         # 从当前位置 index 开始，尝试截取不同长度的数字
#         for i in range(index, n):
#             # 优化：增量计算数值，避免 str 切片和 int() 转换
#             # val = val * 10 + digits[i]
#             val = val * 10 + digits[i]

#             # 剪枝：处理前导零
#             # 如果当前数字长度 > 1 (即 i > index) 且第一个数字是 0 (digits[index] == 0)
#             # 那么这个数字是非法的（如 "05"），直接停止当前层的循环
#             if i > index and digits[index] == 0:
#                 break
            
#             # 递归逻辑
#             if index == 0:
#                 # 第一个数字，前面没有运算符
#                 dfs(i + 1, val, val)
#             else:
#                 # 加法
#                 dfs(i + 1, current_val + val, val)
#                 # 减法
#                 dfs(i + 1, current_val - val, -val)
#                 # 乘法
#                 # 撤销 prev_val 的影响： (current - prev) + (prev * val)
#                 dfs(i + 1, current_val - prev_val + (prev_val * val), prev_val * val)

#     dfs(0, 0, 0)
#     print(ans)

# if __name__ == "__main__":
#     solve()            
                    

            
            
        
    