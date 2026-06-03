import sys
def max_matrix(mar,n):
    pro=[[0]*n for i in range(n)]
    for k,l in enumerate(mar):
        last=0
        for i,j in enumerate(l):
            pro[k][i]=j+last
            last=pro[k][i]
    max_sum = float('-inf')  # 初始化为负无穷
    for j in range(n):
        current_max=0
        for k in range(n):
            a=pro[k][j]
            current_max=max(current_max+a,a)
            max_sum=max(max_sum,current_max)
        if j==0:
            continue
        for i in range(j):
            current_max=0
            for k in range(n):
                a=pro[k][j]-pro[k][i]
                current_max=max(current_max+a,a)
                max_sum=max(max_sum,current_max)
    return max_sum

n=int(sys.stdin.readline())
b=list(map(int,sys.stdin.read().strip().split()))
index=0
mar=[]
for i in range(n):
    l=b[index:index+n]
    mar.append(l)
    index+=n
print(max_matrix(mar,n))


        