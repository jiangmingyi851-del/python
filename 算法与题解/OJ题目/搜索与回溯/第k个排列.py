class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        factorial = [1]
        for i in range(1, n):
            factorial.append(factorial[-1] * i)
        
        k -= 1
        ans = list()
        valid = [1] * (n + 1)
        for i in range(1, n + 1):
            order = k // factorial[n - i] + 1
            for j in range(1, n + 1):
                order -= valid[j]
                if order == 0:
                    ans.append(str(j))
                    valid[j] = 0
                    break
            k %= factorial[n - i]

        return "".join(ans)

import sys
def next_permutation(s):
    n=len(s)
    temp=s[:]
    i=n-2
    while i>=0 and s[i]>=s[i+1]:
        i-=1
    if i<0:
        return list(range(1,n+1))
    j=n-1
    while s[j]<=s[i]:
        j-=1
    temp[i],temp[j]=temp[j],temp[i]
    temp[i+1:]=temp[n-1:i:-1]
    return temp
def main():
    data = sys.stdin.read().splitlines()
    m = int(data[0])
    index = 1
    results = []
    for _ in range(m):
        parts = data[index].split()
        index += 1
        n = int(parts[0])
        k = int(parts[1])
        arr = list(map(int, data[index].split()))
        index += 1
        for _ in range(k):
            arr = next_permutation(arr)
        results.append(" ".join(map(str, arr)))
    
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
#注： 其实也可以用最上面的解法，先反解出d是多少，再求第d+k个排列即可
# 用dfs生成全排列
def dfs(path, used, n, k, res):
    if len(path) == n:
        res.append(path[:])
        return
    for i in range(1, n + 1):
        if not used[i]:
            used[i] = True
            path.append(i)
            dfs(path, used, n, k, res)
            path.pop()
            used[i] = False

