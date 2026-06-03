
from collections import deque


n,m=map(int,input().split())
a=list(map(int,input().split()))
G=[[] for i in range(n+1)]
indeg=[0]*(n+1)
for i in range(m):
    u,v=map(int,input().split())
    G[u].append(v)
    indeg[v]+=1
q=deque()
dp=[0]*(n+1)
cnt=0
for i in range(1,n+1):
    if indeg[i]==0:
        q.append(i)
        dp[i]=a[i]
while q:
    u=q.popleft()
    cnt+=1
    for v in G[u]:
        a[v]=max(dp[v],a[v]+dp[u])
        indeg[v]-=1
        if indeg[v]==0:
            q.append(v)
if cnt!=n:
    print(-1)
else:
    print(max(dp))


    


    