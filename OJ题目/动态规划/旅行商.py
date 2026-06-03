import sys
data=sys.stdin.read().strip().split()
iterator=iter(data)
n=int(next(iterator))
dist=[]
for i in range(n):
        row=list(int(next(iterator)) for _ in range(n))
        dist.append(row)
mask=1<<n
dp=[[float('inf')]*n for _ in range(mask)]
dp[1][0]=0
for i in range(1,n):
    dp[(1<<i)|1][i]=dist[i][0]
for j in range(1,mask,2):
    for i in range(1,n):
        if (not (j>>i)&1) or j^(1<<i)==1:
            continue
        dp[j][i]=min([dp[j^(1<<i)][k]+dist[k][i] for k in range(1,n) if (j&(1<<k) and k!=i)])
ans=float('inf')
for i in range(n):
    dp[mask-1][i]+=dist[i][0]
    if dp[mask-1][i]<ans:
        ans=dp[mask-1][i]
print(ans)


    


