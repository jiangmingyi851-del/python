from collections import deque
n,m=map(int,input().split())
time=list(map(int,input().split()))
next_neighbor=[[] for i in range(n+1)]
indeg=[0]*(n+1)
ve=[0]*(n+1)
for i in range(m):
    a,b=map(int,input().split())
    next_neighbor[a].append(b)
    indeg[b]+=1
q=deque(i for i in range(1,n+1) if indeg[i]==0)
for i in q:
    ve[i]=time[i-1]
stack=[]
while q:
    cur=q.popleft()
    stack.append(cur)
    for v in next_neighbor[cur]:
        ve[v]=max(ve[v],time[v-1]+ve[cur])
        indeg[v]-=1
        if indeg[v]==0:
            q.append(v)
if len(stack)<n:
    print(-1)
    exit()

print(max(ve[1:n+1]))