n,m=map(int,input().split())
graph=[[] for i in range(n+1)]
parent=[i for i in range(n+1)]
visited=[False for i in range(n+1)]
def find(x):
    if parent[x]!=x:
        parent[x]=find(parent[x])
    return parent[x]
def union(x,y):
    parent[find(x)]=find(y)
edges=[]
for i in range(m):
    a,b,cost=map(int,input().split())
    edges.append((cost,a,b))
edges.sort()
ans=0
for cost,a,b in edges:
    if find(a)!=find(b):
        union(a,b)
        ans+=cost
a=find(1)
for i in range(1,n+1):
    if find(i)!=a:
        print('orz')
        exit()
else:
    print(ans)




