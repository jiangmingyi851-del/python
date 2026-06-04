n=int(input())
edges=set()
graph=[[] for i in range(n)]
for i in range(n-1):
    a,b=map(int,input().split())
    edges.add((a,b))
    graph[a].append(b)
    graph[b].append(a)
bann=set(map(int,input().split()))
visited=[0]*n
ans=1
def dfs(x):
    global ans
    for y in graph[x]:
        if y not in bann and visited[y]==0:
            visited[y]=1
            ans+=1
            dfs(y)
visited[0]=1
dfs(0)
print(ans)

