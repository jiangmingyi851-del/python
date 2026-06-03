n,m=map(int,input().split())
cost=list(map(int,input().split()))
graph=[[] for i in range(n+1)]
for i in range(m):
    a,b=map(int,input().split())
    graph[a].append(b)
    graph[b].append(a)
visited=[0]*(n+1)
comp_list=[]
def dfs(v,comp):
    for u in graph[v]:
        if visited[u]==0:
            visited[u]=1
            comp.append(u)
            dfs(u,comp)
for i in range(1,n+1):
    if visited[i]==0:
        comp=[]
        dfs(i,comp)
        comp_list.append(comp)
ans=0
for comp in comp_list:
    ans+=min(cost[i-1] for i in comp)
print(ans)