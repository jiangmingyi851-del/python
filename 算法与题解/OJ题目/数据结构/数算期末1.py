import sys
from collections import deque
from collections import defaultdict
n,m=map(int,input().split())
nxt=[0]*(n+2)
pre=[0]*(n+2)
for i in range(1,n+1):
    nxt[i]=i+1
    pre[i]=i-1
nxt[0]=1
pre[0]=0
nxt[n+1]=n+1
pre[n+1]=n
comp=[0]*(n+1)
comp_cnt=0
s=sys.stdin.readlines()
vall=defaultdict(int)
adj=[[] for _ in range(n+1)]
edges=[]
for l in s:
    u,v,val=map(int,l.split())
    edges.append((u,v,val))
    adj[u].append(v)
    adj[v].append(u)
queue=deque()
parent=[i for i in range(n+1)]
while nxt[0]!=n+1:
    comp_cnt+=1
    queue.append(nxt[0])
    start=nxt[0]
    p=pre[start]
    nx=nxt[start]
    pre[nx]=p
    nxt[p]=nx
    comp[start]=comp_cnt
    while queue:
        u=queue.popleft()
        banned=set(adj[u])
        cur=nxt[0]
        while cur < n+1:
            cur_nxt=nxt[cur]
            if cur not in banned:
                queue.append(cur)
                comp[cur]=comp_cnt
                parent[cur]=u
                a=nxt[cur]
                b=pre[cur]
                nxt[b]=a
                pre[a]=b
            cur=cur_nxt
line=[]
def find(u):
    while parent[u]!=u:
        parent[u]=parent[parent[u]]
        u=parent[u]
    return u
for u,v,val in edges:
    if comp[u]!=comp[v]:
        line.append((val,comp[u],comp[v]))

line.sort()
ans=0
for val,u,v in line:
    a,b=find(u),find(v)
    if a!=b:
        ans+=val
        parent[a]=b
print(ans)
        
        

        
            



        



        

